from django.shortcuts import HttpResponse


def report(request):
    if request.method == "POST":
        asset_data = request.POST.get('asset_data')
        print(asset_data)
        return HttpResponse("成功收到数据！")
