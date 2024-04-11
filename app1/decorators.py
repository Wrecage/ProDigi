# from django.shortcuts import redirect

# def prevent_logged_in_users(view_func):
#     def _wrapped_view(request, *args, **kwargs):
#         if request.user.is_authenticated:
#             # If the user is already logged in, redirect to the home page or any other appropriate page
#             return redirect('home')  # Change 'home' to the appropriate URL name for your home page
#         return view_func(request, *args, **kwargs)
#     return _wrapped_view