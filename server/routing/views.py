import json

from django.shortcuts import render
from django.http import HttpResponse
from .models import Routes

from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect


# @method_decorator(ensure_csrf_cookie, name='dispatch')
# class GetCSRFToken(APIView):
#     # permission_ctasses = ( )

#     def get(setf, request, format=None):
#         return HttpResponse({'success': 'CSRF cookie set'})


# @method_decorator(csrf_protect, name='dispatch')
# # Create your views here.
def sendHTML(request):
    # if request.method == "POST":
    return HttpResponse("<h1>Hello World</h1>")


def serialize_link(route: Routes):
    return {
        "id": route.id,
        "identifier": route.identifier,
        "link": route.link,
    }


def get_post_data(request):
    if request.method == "GET":
        array = [serialize_link(i) for i in Routes.objects.all()]
        send = {"ok": True, "packet": array}
        return HttpResponse(content=json.dumps(send))


def create_link_data(request):
    if request.method == "POST":
        body = json.loads(request.body)
        # Routes.objects.create(identifier=body.identifier, link=body.link)
        obj = Routes(
            identifier=body['identifier'].strip(), link=body['link'].strip())
        obj.save()
        print(obj.id)
        send = {"ok": True, "msg": 'Successfully created'}
        return HttpResponse(content=json.dumps(send))
    if request.method == "PATCH":
        body = json.loads(request.body)
        print("id" in body)
        check = body.get('id', False)

        if not check:
            send = {"ok": False, "msg": "ID is not available"}
            return HttpResponse(content=json.dumps(send))
        obj = Routes.objects.get(id=body['id'])

        obj.identifier = body['identifier']
        obj.link = body['link']

        obj.save()

        send = {"ok": True, "msg": "Update successfully"}
        return HttpResponse(content=json.dumps(send))


def delete_link_data(request, id):
    if request.method == "DELETE":
        record_to_delete = Routes.objects.get(id=id)
        record_to_delete.delete()

        send = {"ok": True, "msg": 'Route deleted'}
        return HttpResponse(content=json.dumps(send))


def get_link(request, identifier):
    if request.method == "GET":
        route_data = Routes.objects.filter(identifier=identifier).first()
        if route_data:
            send = {"ok": True,  "packet": serialize_link(route_data)}
            return HttpResponse(content=json.dumps(send))
        else:
            send = {"ok": False,
                    "msg": f"Object with identifier '{identifier}' not found"}
            return HttpResponse(content=json.dumps(send))


def get_link_id(request, id):
    if request.method == "GET":
        route_data = Routes.objects.get(id).first()
        if route_data:
            send = {"ok": True,  "packet": serialize_link(route_data)}
            return HttpResponse(content=json.dumps(send))
        else:
            send = {"ok": False,
                    "msg": f"Object with id '{id}' not found"}
            return HttpResponse(content=json.dumps(send))
