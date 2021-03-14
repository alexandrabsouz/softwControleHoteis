from flask_restful import Resource, reqparse
from models.hotel import HotelModel


hoteis = [{ 'hotel_id': 'alpha',
            'nome': 'Alpha Hotel',
            'estrelas': 4.3,
            'diaria': 420.34,
            'cidade': 'Rio de Janeiro'},

            {'hotel_id': 'bravo',
            'nome': 'Bravo Hotel',
            'estrelas': 4.4,
            'diaria': 380.90,
            'cidade': 'Santa Catarina'},

            {'hotel_id': 'charlie',
            'nome': 'Charlie Hotel',
            'estrelas': 3.9,
            'diaria': 320.20,
            'cidade': 'Santa Catarina'}]



class Hoteis(Resource):
    def get(self):
        return {'hoteis': [hotel.json() for hotel in HotelModel.query.all()]}

class Hotel(Resource):
    atributos = reqparse.RequestParser()
    atributos.add_argument('nome', type=str, required=True, help='O campo NOME não pode ficar vazio')
    atributos.add_argument('estrelas', type=str, required=True, help='O campo ESTRELAS não pode ficar vazio')
    atributos.add_argument('diaria')
    atributos.add_argument('cidade')


    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {'messege': 'Hotel not found'}, 404 #Error


    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {'menssagem': f'{hotel_id} já existe'}, 400 #Requisição errada
        dados = Hotel.atributos.parse_args()
        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            return {'message': 'Não foi possivel salvar os dados hotel, tente novamente'}, 500 #Problema interno no servidor
        return hotel.json(), 200 # Adiciona o hotel a lista com sucesso


    def put(self, hotel_id):
        dados = Hotel.atributos.parse_args()
        hotel_encontrado = HotelModel.find_hotel(hotel_id)


        if hotel_encontrado:
            hotel_encontrado.update_hotel(**dados)
            try:
                hotel_encontrado.save_hotel()
            except:
                return {'message': 'Não foi possivel salvar os dados hotel, tente novamente'}, 500 #Problema interno no servidor
            return hotel_encontrado.json(), 200 # Tudo ok


        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            return {'message': 'Não foi possivel salvar os dados hotel, tente novamente'}, 500 #Problema interno no servidor
        return hotel.json(), 201 # Criado com sucesso



    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            try:
                hotel.delete_hotel()
            except:
                return {'message': 'Não foi possivel deletar hotel, tente novamente'}, 500 #Problema interno no servidor
            return {'message': 'Hotel Deletado.'}
        return {'message': 'Hotel não existe'}
