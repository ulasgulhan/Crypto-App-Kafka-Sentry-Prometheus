from django.shortcuts import redirect, render


def landing(request):
    if request.user.is_authenticated:
        return redirect('all_data')
    else:
        return render(request, 'landing.html')