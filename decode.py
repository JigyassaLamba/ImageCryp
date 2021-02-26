import os, sys
from PIL import Image
from utils import convert

def main():

	if len(sys.argv) < 2 or len(sys.argv) > 3:
		print("DECODING")
		return
	if len(sys.argv) >= 2:
		img_path = sys.argv[1]
	if len(sys.argv) >= 3:
		op_path = sys.argv[2]
		fname, fext = os.path.splitext(op_path)
		op_path = fname + '.png'
	else:
		op_path = 'images/decoded_image.png'
	decoded_image = decode(Image.open(img_path))
	decoded_image.save(op_path)

def extract(image,width1,height1, count):
	encoded_pix = ''
	k = 0
	for i in range(width1):
		for j in range(height1):
			if j == 0 and i == 0:
				continue
			r, g, b = image[i, j]
			red_b, green_b, blue_b = convert(r, g, b)
			encoded_pix += red_b[4:8] + green_b[4:8] + blue_b[4:8]
			if k >= count * 2:
				return encoded_pix
	return encoded_pix

def make_img(img_pix, width, height):
	image = Image.new("RGB", (width, height))
	image_copy = image.load()
	k = 0
	for i in range(width):
		for j in range(height):
			red_b = img_pix[k:k+8]
			green_b = img_pix[k+8:k+16]
			blue_b = img_pix[k+16:k+24]
			image_copy[i, j] = (int(red_b, 2), int(green_b, 2), int(blue_b, 2))
			k += 24
	return image
	
def decode(image):
	image_copy = image.load()
	width1,height1 = image.size
	r, g, b = image_copy[0, 0]
	red_b, green_b, blue_b = convert(r, g, b)
	w_h_binary = red_b + green_b + blue_b
	width_hidden = int(w_h_binary[0:12], 2)
	height_hidden = int(w_h_binary[12:24], 2)
	count = width_hidden * height_hidden
	encoded_pix = extract(image_copy,width1,height1, count)
	decoded_image = make_img(encoded_pix, width_hidden, height_hidden)
	return decoded_image

if __name__ == '__main__':
	main()