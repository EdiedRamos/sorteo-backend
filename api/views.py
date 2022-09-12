from django.views import View
from .models import Company
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json

# helpers
def getById(id):
  companies = list(Company.objects.filter(nit = id).values())
  return companies

# class for managing the company data
class CompanyView(View):
  # override dispatch method for avoiding csrf protection
  @method_decorator(csrf_exempt)
  def dispatch(self, request, *args, **kwargs):
    return super().dispatch(request, *args, **kwargs)
  
  # get rest method
  def get(self, request, nit = -1):
    if ~nit:
      companies = getById(nit)
      if len(companies) > 0:
        result = {
          'message': 'success',
          'company': companies[0]
        }
      else:
        result = {
          'message': 'Empresa no encontrada'
        }
    else:
      companies = list(Company.objects.values())
      result = {
        'message': 'success',
        'companies': companies
      }
    return JsonResponse(result)
  
  # post rest method
  def post(self, request):
    post_data = json.loads(request.body)
    # checking for duplicate nit
    check = getById(post_data.get('nit'))
    if len(check) > 0:
      return JsonResponse({
        'message': 'La empresa ya se encuentra registrada'
      })
    # registering the company
    Company.objects.create(
      name = post_data.get('name'),
      address = post_data.get('address'),
      nit = post_data.get('nit'),
      phone = post_data.get('phone')
    )
    data = {
      'message': 'Empresa registrada'
    }
    return JsonResponse(data)
  
  # put rest method
  def put(self, request, nit = -1):
    # check if the company exists
    check = getById(nit)
    
    if len(check) == 1:
      put_data = json.loads(request.body)
      # checking for duplicate nit if the current nit is different
      if put_data.get('nit') != str(nit):
        check = getById(put_data.get('nit'))
        if len(check) > 0:
          return JsonResponse({
            'message': 'No puedes usar ese NIT'
          })
      # updating the values
      company = Company.objects.get(nit = nit)
      company.name = put_data.get('name')
      company.address = put_data.get('address')
      company.nit = put_data.get('nit')
      company.phone = put_data.get('phone')
      # saving the values
      company.save()
      
      return JsonResponse({
        'message': 'Los datos han sido actualizados'
      })
    else:
      return JsonResponse({
        'message': 'La empresa no está registrada'
      })
  
  #delete rest method
  def delete(self, request, nit = -1):
    if ~nit:
      # checking if the company is registered
      check = getById(nit)
      if len(check) == 0:
        return JsonResponse({
          'message': 'La empresa no está registrada'
        })
      deleted = Company.objects.filter(nit = nit).delete()
      print(deleted)
      return JsonResponse({
        'message': 'La empresa ha sido eliminada'
      })
    else:
      return JsonResponse({
        'message': 'not necesary for the tecnhical test'
      })
    