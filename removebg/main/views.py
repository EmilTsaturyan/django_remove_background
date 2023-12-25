from django.shortcuts import render
from rembg import remove
from PIL import Image
from .forms import ImageUploadForm
from django.http import HttpResponse
from io import BytesIO

# Create your views here.

def remove_bg(image):
    input = Image.open(image)
    output = remove(input)
    return output

def index(request):

    processed_image = None

    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = form.cleaned_data['image']
            processed_image = remove_bg(uploaded_image)
            processed_image_io = BytesIO()
            processed_image.save(processed_image_io, format='PNG')
            processed_image_io.seek(0)

            return HttpResponse(processed_image_io, content_type='image/png')
    else:
        form = ImageUploadForm()

    return render(request, 'index.html', {'processed_image': processed_image})

