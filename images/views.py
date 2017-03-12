import os
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
import string
from images.models import Tokens, Images
import random
import pylzma
from django.conf import settings
from cStringIO import StringIO
from django.http import HttpResponse
from rest_framework.decorators import api_view
from images.serializers import TokensSerializer, ImagesSerializer
from multiprocessing import Pool

# Create your views here.
class Gen_Token(APIView):
	"""docstring for Gen_Token"""
	def get(self, request, format = None):
		tok =  ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(20))
		t = Tokens(token = tok)
		t.save()
		serializer = TokensSerializer(t, many = False)
		return Response(serializer.data, status = 201)

class ImageView(APIView):
	"""docstring for ImageVIew"""
	def get(self, request,format = None):
		filename = request.GET['filename']
		image = Images.objects.filter(filename = filename).first()
		if image is None:
			return Response({'detail': 'Invalid Filename'},status = 404)
		namef = open(settings.IMAGES_ROOT+'/'+filename+'.'+'compr', 'r+')
		filecontent = namef.read()
		uncomp = pylzma.decompress(filecontent)
		ext = filename.rsplit('.',1)[1].lower()
		return HttpResponse(uncomp, content_type = 'image/'+ext)

class Index(APIView):
	"""docstring for Index"""
	def post(self, request, format = None):
		token = request.POST.get('token','')
		if Tokens.objects.filter(token = token).first() is not None:
			file =  request.FILES['file']
			orignal_name = file.__str__()
			org_size = file._size
			if file._size > 26214400:
				return Response({"detail":"File Size Too Large"},status = 413)
			img = Images.objects.filter(orignal_name = orignal_name).first()
			if img is None:
				compressed_obj = pylzma.compressfile(file)
				compressed = ''
				while True:
					tmp = compressed_obj.read(1)
					if not tmp:
						break
					compressed += tmp
				new_file_name = ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(20))+'.'+file.__str__().rsplit('.',1)[1].lower()
				if Images.objects.filter(filename = new_file_name).first() is None:
					namef = settings.IMAGES_ROOT+'/'+new_file_name+'.'+'compr'
					with open(namef, 'w') as cfile:
						cfile.write(compressed)
					ns = os.path.getsize(namef)
					cr = (1-(float(ns)/float(org_size)))*100
					image = Images(token = token, orignal_name = orignal_name, filename = new_file_name, path = namef, compression_percentage = cr)
					image.save()
					serializer = ImagesSerializer(image, many = False)
					return Response(serializer.data,status = 201)
			else:
				serializer = ImagesSerializer(img, many = False)
				return Response(serializer.data,status = 302)
		else:
			return Response({'detail':'Authorization failed'},status = 401)
	def delete(self, request, format = None):
		try:
			body = getBody(request.body)
		except Exception as e:
			return Response({'detail': 'Bad Request'},status = 400)
		
		token = body['token']
		if Tokens.objects.filter(token = token).first() is not None:
			filename = body['filename']
			if filename is not None:
				i = Images.objects.filter(filename = filename).first()
				if i is not None:
					i.delete()
				else:
					return Response({'detail':'Invalid Filename'},status = 404)
				return Response(status = 200)
			else:
				return Response({'detail': 'Filename not Received'},status = 204)
		else :
			return Response({'detail':'Authorization failed'},status = 401)
	
	def patch(self, request, format = None):
		token = request.data['token']
		if Tokens.objects.filter(token = token).first() is not None:
			image = Images.objects.filter(filename = request.data['filename']).first()
			if image is not None:
				file =  request.FILES['file']
				orignal_name = file.__str__()
				org_size = file._size
				if file._size > 26214400:
					return Response({"detail":"File Size Too Large"},status = 413)
				compressed_obj = pylzma.compressfile(file)
				compressed = ''
				while True:
					tmp = compressed_obj.read(1)
					if not tmp:
						break
					compressed += tmp
				namef = settings.IMAGES_ROOT+'/'+request.data['filename']+'.'+'compr'
				with open(namef, 'w') as cfile:
					cfile.write(compressed)
				ns = os.path.getsize(namef)
				cr = (1-(float(ns)/float(org_size)))*100
				image.delete()
				image = Images(token = token, orignal_name = orignal_name, filename = request.data['filename'], path = namef, compression_percentage = cr)
				image.save()
				print "hello"
				serializer = ImagesSerializer(image, many = False)
				return Response(serializer.data,status = 201)
			else:
				return Response({'detail': 'Filename not known'},status = 404)
		else:
			return Response({'detail': 'Authorization failed'},status = 401)

def getBody(c):
		body = c.split('&')
		a = []
		b = {}
		for i in body:
			a.append(i.split('='))
		for i in a:
			b[i[0]] = i[1]
		return b
