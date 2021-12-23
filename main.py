# The order server maintains
# a list of all orders received for the books.
import json

from flask import Flask, abort, request, json, jsonify
import requests

app = Flask(__name__)

@app.route('/purchase/<int:id>', methods=['POST'])
def purchase(id):
    reqGET = requests.get('http://192.168.56.101:7000/info/{}'.format(id))

    if reqGET.status_code == 200:
        dataDictionary = reqGET.json()  # content of json as dictionary
        if dataDictionary['quantity'] < 1:
            return 'Quantity can not be less than 1', 406
        else:
            #requests.post('http://192.168.56.103:9000/purchase/{}'.format(id), json=(dataDictionary))

            dataDictionary['quantity'] = dataDictionary['quantity'] - 1

            reqPUT = requests.put('http://192.168.56.101:7000/updateinfo/{}'.format(id), json=(dataDictionary))
            print(reqPUT.status_code)
            if reqPUT.status_code == 200:
                print('fjvivffjjvvvvvvvvvvvvvvv')
                # The order server maintains
                # a list of all orders received for the books.
                f = open('ListOfOrders.json', 'r+')

                data = json.load(f)# return json obj
                # for
                data.append({'id': id, 'title': dataDictionary['title'], 'price': dataDictionary['price']})
                f.close()
                f2 = open('ListOfOrders.json', 'w')
                # to save python obj into file:
                json.dump(data, f2)# python -->json
                f2.close()
                #requests.post('http://192.168.56.103:9000/purchase/'.format(id), json=(dataDictionary))

                return jsonify({'id': id, 'title': dataDictionary['title'], 'price': dataDictionary['price']})
            elif reqPUT.status_code == 404:
                return 'The server has not found anything matching the given URL', reqPUT.status_code

            else:
                return 'Status code ' +str(reqPUT.status_code)+' indicates to something ERROR!', reqPUT.status_code


    elif reqGET.status_code == 404:
        return 'The server has not found anything matching the given URL', 404

    else:
        return 'Status code ' + str(reqGET.status_code) + ' indicates to something ERROR!', reqGET.status_code


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9999)