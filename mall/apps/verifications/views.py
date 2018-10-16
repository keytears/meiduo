from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.views import APIView
from libs.captcha.captcha import captcha
from django_redis import get_redis_connection

# Create your views here.


class RegisterImageCodeView(APIView):
    """
    生成验证码
    GET     verifications/imagecodes/(?P<image_code_id>.+)/
    通过js生成一个uuid(image_code_id)
    """
    def get(self, request, image_code_id):
        """
        通过captcha库生成图片验证码，并保存到redis，然后返回前端

        1.创建验证码和图片
        2.保存到redis
        3.返回前端数据
        """

        # 创建图片验证码
        text, image = captcha.generate_captcha()

        # 保存到redis
        # 1.连接redis
        redis_conn = get_redis_connection("code")
        # 2.保存到redis
        redis_conn.setex('image_%s'%image_code_id, 60, text)

        # 图片返回前端
        # 注意,图片是二进制,我们通过HttpResponse返回
        return HttpResponse(image, content_type='image/jpeg')


        pass
