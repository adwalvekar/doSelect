# doSelect
An Image API for the needs of the Internet.(_This is a solution submission for an Internship test_)
## Usage:
<br>
### GENERAL INFORMATION
I highly recommend using [POSTMAN](https://www.getpostman.com/). Makes the whole experience very seamless.
All the image Requests are to be made to the endpoint `/api/images`. The HTTP requests used in this app are `POST`, `GET`, `DELETE`, `PATCH`
<br>
### Generating a Token
Before being able to make any requests, you will need to generate a token. Make a `GET` Request to the endpoint `/api/images/gen_token` to first generate a unique token. This token needs to be used with all the requests. (I understand that this is not safe for prod, but I needed a way to generate a token)
The response will be in the form of usual JSON:
<br>
```
{
  "token": "WENQA7Y2THPYG5P2IYG7"
}

Status Code: 201
```
<br>
### Using the Actual API
<br>
###### Uploading an image:
Make a `POST` request to  `/api/images`. The parameters are :
```
token: Uniquely generated Token from the previous section
file: The Actual File Itself

```
<br>
On Successful Upload, you will receive JSON like so:

```
{
  "token": "WENQA7Y2THPYG5P2IYG7",
  "filename": "r2bj46h23i241x7uljkd.jpg",
  "compression_percentage": 0.574164408777178
}
Status Code: 201
```
<br>
If the same image is being uploaded, you will receive the following:
```
{
  "token": "WENQA7Y2THPYG5P2IYG7",
  "filename": "r2bj46h23i241x7uljkd.jpg",
  "compression_percentage": 0.574164408777178
}
Status Code: 302
```
<br>
###### Deleting an image:
Make a `DELETE` request to  `/api/images`. The parameters are :
```
token: Uniquely generated Token from the previous section
filename: The name of the file received once the POST request was successfully made

```
<br>
On successful deletion, you will receive only a status like so:

```
Status Code: 200
```
<br>
###### Updating an image:
Make a `PATCH` request to  `/api/images`. The parameters are :
```
token: Uniquely generated Token from the previous section
filename: The name of the file received once the POST request was successfully made
file: The actual Image file to be replaced with
```
<br>
On successful updation, you will receive only a status like so:

```
Status Code: 201
```
<br>
### Viewing an Image
<br>
The uploaded images can be viewed at the endpoint `/api/images/view_image?filename=filenameGenerated.jpg`.<br>
On request, the compressed image is uncompressed and rendered as a normal image.

## Technical Details:
<br>
The image compression is achieved by storing it as a filename.jpg.cmpr file. The compression used is LZMA compression. Although this is not asynchronous, as Django doesn't behave very well with Python's built in async pool, the compression rates achieved for some images are very high. I have seen compression ratios as high as 7%!
Please contact me on aditya.s.walvekar@gmail.com for any details.

Cheers!