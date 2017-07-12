from django.shortcuts import render, render_to_response


def handler404(request):
    return render(request, '404.html', status=404)

def paralle_test1():
    print('hello')
    with open('/home/maksim/venv/qinggang/managesys/QinggangManageSys/test_crontab.txt','a') as f:
        f.write("hello\n")
