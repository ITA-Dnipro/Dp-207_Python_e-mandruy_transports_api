from klein import Klein, Response
import json
from spider_runner import SpiderRunner
from transport_scraper.transport_scraper.spiders.ip_test import IpTestSpider
from transport_scraper.transport_scraper.\
    spiders.poezdato_blablacars import PoezdatoBlablacarsSpider
from transport_scraper.transport_scraper.\
    spiders.poezd_ua import PoezdUaSpider
from api_utils.jwt_helpers import (
    is_valid_jwt_token, jwt_error_response
)


app = Klein()


def return_spider_output(output):
    '''
    Return json Klein Response from a scrapy spider
    '''
    output = json.dumps(output)
    respose = Response(
        headers={'Content-Type': 'application/json'},
        body=output.encode(),
        code=200
    )
    return respose


@app.route('/ip_test')
def ip_test(request):
    runner = SpiderRunner()
    deferred = runner.crawl(IpTestSpider)
    deferred.addCallback(return_spider_output)
    return deferred


def error_405():
    error_msg = {'msg': 'method not allowed', 'code': 405}
    error_msg = json.dumps(error_msg)
    return Response(
        headers={'Content-Type': 'application/json'},
        body=error_msg.encode(),
        code=405
    )


@app.route('/api/v.1.0/cars')
def poezdato_blablacars(request):
    if request.method != b"POST":
        return error_405()
    # jwt check
    auth_token = request.getHeader('authorization')
    jwt_check = is_valid_jwt_token(auth_token)
    if jwt_check is not True:
        return jwt_error_response(jwt_check)
    #
    json_payload = json.loads(request.content.read())
    #
    runner = SpiderRunner()
    deferred = runner.crawl(
        PoezdatoBlablacarsSpider,
        departure_name=json_payload['departure_name'],
        departure_date=json_payload['departure_date'],
        arrival_name=json_payload['arrival_name']
    )
    deferred.addCallback(return_spider_output)
    return deferred


@app.route('/api/v.1.0/trains')
def poezd_ua(request):
    if request.method != b"POST":
        return error_405()
    # jwt check
    auth_token = request.getHeader('authorization')
    jwt_check = is_valid_jwt_token(auth_token)
    if jwt_check is not True:
        return jwt_error_response(jwt_check)
    #
    json_payload = json.loads(request.content.read())
    #
    runner = SpiderRunner()
    deferred = runner.crawl(
        PoezdUaSpider,
        departure_name=json_payload['departure_name'],
        departure_date=json_payload['departure_date'],
        arrival_name=json_payload['arrival_name']
    )
    deferred.addCallback(return_spider_output)
    return deferred


if __name__ == "__main__":
    app.run('0.0.0.0', 4500)
