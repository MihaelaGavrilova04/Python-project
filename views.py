from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth #auth to authenticate the user
from django.contrib import messages #to send a message to the frontend
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required #to direct the user to the login page and not give him access to the page
from .models import Profile, Post, LikePost, FollowersCount
from itertools import chain
import random #to suggest users randomly

# Create your views here.

@login_required(login_url='signin') #the url where it should redirect the user into if he is not logged in
def index(request):
    user_object = User.objects.get(username = request.user.username) #the object of the currently logged user
    user_profile = Profile.objects.get(user = user_object)
#now that i have the object, i use it to get the profile
    user_following_list = []
    feed = []
#feed will contain the posts of the people the user is following
    user_following = FollowersCount.objects.filter(follower=request.user.username) #get the objects of all the users that the user is following

    for users in user_following:
        user_following_list.append(users.user)

    for usernames in user_following_list:
        feed_lists = Post.objects.filter(user=usernames) #getting the posts of the people we are following
        feed.append(feed_lists)
#query set? which we want to convert to list to use in the template
    feed_list = list(chain(*feed)) #new var, chain will convert it to a list

    # user suggestion starts
    all_users = User.objects.all()
    user_following_all = []

    for user in user_following: #adding all of the users this profile follows
        user_list = User.objects.get(username=user.user)
        user_following_all.append(user_list)
#the suggestions will be if the profile is in all users and is not in the already following
    new_suggestions_list = [x for x in list(all_users) if (x not in list(user_following_all))]
    current_user = User.objects.filter(username = request.user.username) #to remove the current user from current_user & not suggest him to himself
    final_suggestions_list = [x for x in list(new_suggestions_list) if ( x not in list(current_user))]
    random.shuffle(final_suggestions_list)

    username_profile = []
    username_profile_list = []

    for users in final_suggestions_list:
        username_profile.append(users.id)

    for ids in username_profile:
        profile_lists = Profile.objects.filter(id_user=ids)
        username_profile_list.append(profile_lists)

    suggestions_username_profile_list = list(chain(*username_profile_list))

                                                              #sending the variable user_profile to the html
    return render(request, 'index.html', {'user_profile': user_profile, 'posts':feed_list, 'suggestions_username_profile_list': suggestions_username_profile_list[:4]})

@login_required(login_url='signin')
def upload(request):

    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']

        new_post = Post.objects.create(user = user, image = image, caption = caption)
        new_post.save()
        return redirect('/')
    else:
        return redirect('/') #return to the homepage


@login_required(login_url='signin') #the user should be logged in to search
def search(request):
    user_object = User.objects.get(username=request.user.username) #get the current user object & its profile
    user_profile = Profile.objects.get(user=user_object)

    if request.method == 'POST': #get the username the person searched
        username = request.POST['username']
        username_object = User.objects.filter(username__icontains=username)#getting list if we enter tom, it will filter all the users which names contain tom

        username_profile = []
        username_profile_list = []

        for users in username_object:
            username_profile.append(users.id)

        for ids in username_profile:
            profile_lists = Profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_lists)

        username_profile_list = list(chain(*username_profile_list))#update it with itself?
    return render(request, 'search.html', {'user_profile': user_profile, 'username_profile_list': username_profile_list})

@login_required(login_url='signin')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id = post_id)
    #has the user already liked the posr(if there is an object in db in which the post id = curr post & user name == curr loged in user => so its already liked
    like_filter = LikePost.objects.filter(post_id = post_id, username = username).first() #the first one, because without .first it will give us a list back with 1 el only
#.filter, not .get so it doesnt throw an error
    if like_filter == None: #hasnt liked the post yet, he can like it
        new_like = LikePost.objects.create(post_id = post_id, username = username)
        new_like.save()
        post.no_of_likes = post.no_of_likes+1 #to count the number of likes fom the module.py
        post.save()
        return redirect('/')
    else: #if the user already liked this post, he can unlike it
        like_filter.delete() #delete the object from the list
        post.no_of_likes = post.no_of_likes-1 #decrease num of likes
        post.save()
        return redirect('/')

@login_required(login_url='signin')
def profile(request, pk): #pk is what is collected from url.py the key and the datatype is a string
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object) #now that we have the user object we can get his profile
    user_posts = Post.objects.filter(user=pk) #we filter the posts from the db that the user = pk (the username of the currently viewed user) because in models.py in class post the user is just a char field with username
    user_post_length = len(user_posts) #the amount of posts of the user

    follower = request.user.username #the person that is following
    user = pk
    if FollowersCount.objects.filter(follower = follower, user = user).first(): #if it is already in the database
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'

    user_followers = len(FollowersCount.objects.filter(user=pk))#getting the followers count module and filtering the ones in which the user(being follower) is pq
    user_following = len(FollowersCount.objects.filter(follower=pk))

    context = { #because we need to pass a lot of stuff, it is more organized to group it as context
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_length': user_post_length,
        'button_text': button_text,
        'user_followers': user_followers,
        'user_following': user_following,
    }
    return render(request, 'profile.html', context)

@login_required(login_url='signin')
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']
        # the first person in the list .filter so it doesnt throw error, the person already follows the other prrson, so he want to unfollow

        if FollowersCount.objects.filter(follower=follower, user=user).first():
            delete_follower = FollowersCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect('/profile/'+user) #back to the profile page of the specific person
        else: #he really wants to follow the person
            new_follower = FollowersCount.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect('/profile/'+user)
    else:
        return redirect('/')

@login_required(login_url='signin')
def settings(request):
    user_profile = Profile.objects.get(user=request.user) #we are getting a particular obj in which the user is the currently authenticaated user

    if request.method == 'POST':

        if request.FILES.get('image') == None: #ако не е предоставена снимка
            image = user_profile.profileimg #слагаме си текущата
            bio = request.POST['bio'] #взимаме инфото и локацията
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        if request.FILES.get('image') != None: #ако подава снимка
            image = request.FILES.get('image') # .FILES because we are dealing with files
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()

        return redirect('settings')
    return render(request, 'setting.html', {'user_profile': user_profile}) #pass that into our html view

def signup(request):

    if request.method == 'POST':
        username = request.POST['username'] #the data posted here is going to get the data from the input in the html code field
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2: #if we go to the user module & we find an object with the email already exists, then it is already taken and we should be changed, it is already taken
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup') #to enter a new email
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            else: #no errors, create the new user
                user = User.objects.create_user(username=username, email = email, password=password)
                user.save() #потребителят се запазва в базата данни по подразбиране на Django, която обикновено е SQLite

                #log user in and go to settings page so he can fill his info
                user_login = auth.authenticate(username = username, password = password)
                auth.login(request, user_login)

                #create a Profile object for the new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('settings') #redirect the user to the settings page to fill his info
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('signup') #failed to sign up, so try again

    else:
        return render(request, 'signup.html')

def signin(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username = username, password = password)
        #we have such a user in our database
        if user is not None:
            auth.login(request, user)
            return redirect('/') #redirect to the homepage
        else:
            messages.info(request, 'No such user')
            return redirect('signin')#redirect the user so he can sign in

    else:
        return render(request, 'signin.html')

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')