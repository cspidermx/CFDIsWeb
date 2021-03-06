from webapp import wappdb


class CFDI(wappdb.Model):
    # UUID varchar | version FLOAT | serie varchar | folio varchar | fecha TIMESTAMP | sello varchar |
    # formapago varchar | nocertificado varchar | certificado varchar | condicionesdepago varchar |
    # subtotal FLOAT | descuento  FLOAT | moneda varchar | tipocambio FLOAT | total FLOAT |
    # tipodecomprobante varchar | metodopago varchar | lugarexpedicion varchar | confirmacion varchar |
    # valida varchar | path varchar
    __bind_key__ = 'cfdi'
    uuid = wappdb.Column(wappdb.String, primary_key=True)
    version = wappdb.Column(wappdb.Float)
    serie = wappdb.Column(wappdb.String)
    folio = wappdb.Column(wappdb.String)
    fecha = wappdb.Column(wappdb.DateTime)
    sello = wappdb.Column(wappdb.String)
    formapago = wappdb.Column(wappdb.String)
    nocertificado = wappdb.Column(wappdb.String)
    certificado = wappdb.Column(wappdb.String)
    condicionesdepago = wappdb.Column(wappdb.String)
    subtotal = wappdb.Column(wappdb.Float)
    descuento = wappdb.Column(wappdb.Float)
    moneda = wappdb.Column(wappdb.String)
    tipocambio = wappdb.Column(wappdb.Float)
    total = wappdb.Column(wappdb.Float)
    tipodecomprobante = wappdb.Column(wappdb.String)
    metodopago = wappdb.Column(wappdb.String)
    lugarexpedicion = wappdb.Column(wappdb.String)
    confirmacion = wappdb.Column(wappdb.String)
    valida = wappdb.Column(wappdb.String)
    path = wappdb.Column(wappdb.String)


class Receptor(wappdb.Model):
    # UUID varchar | RFC varchar | nombre varchar | residenciafiscal varchar | numregidtrib varchar | usoCFDI varchar
    __bind_key__ = 'cfdi'
    uuid = wappdb.Column(wappdb.String, primary_key=True)
    RFC = wappdb.Column(wappdb.Float)
    nombre = wappdb.Column(wappdb.String)
    residenciafiscal = wappdb.Column(wappdb.String)
    numregidtrib = wappdb.Column(wappdb.String)
    usoCFDI = wappdb.Column(wappdb.String)


class Emisor(wappdb.Model):
    # UUID varchar | RFC varchar | nombre varchar | regimenfiscal varchar
    __bind_key__ = 'cfdi'
    uuid = wappdb.Column(wappdb.String, primary_key=True)
    RFC = wappdb.Column(wappdb.Float)
    nombre = wappdb.Column(wappdb.String)
    regimenfiscal = wappdb.Column(wappdb.String)


class Aerolineas(wappdb.Model):
    # UUID varchar | id varchar | Version float | TUA float | TotalOtrosCargos float |
    __bind_key__ = 'cfdi'
    uuid = wappdb.Column(wappdb.String, primary_key=True)
    id = wappdb.Column(wappdb.String)
    Version = wappdb.Column(wappdb.Float)
    TUA = wappdb.Column(wappdb.Float)
    TotalOtrosCargos = wappdb.Column(wappdb.Float)


class AerolineasOtrosCargos(wappdb.Model):
    # CodigoCargo varchar | Importe float | id varchar
    __bind_key__ = 'cfdi'
    __tablename__ = 'Aerolineas_OtrosCargos'
    CodigoCargo = wappdb.Column(wappdb.String, primary_key=True)
    Importe = wappdb.Column(wappdb.Float, primary_key=True)
    id = wappdb.Column(wappdb.String, primary_key=True)


class Articulo69(wappdb.Model):
    #   rfc	varchar | nombre varchar | situacion varchar | numofi_presuncion varchar | fechaofi_presuncion datetime |
    # 	numofi_desvirtuado varchar | fechaofi_desvirtuado datetime | numofi_definitivo varchar |
    # 	fechaofi_definitivo datetime | numofi_sentfav varchar | fechaofi_sentfav datetime
    __bind_key__ = 'art69b'
    __tablename__ = 'satart69b'
    rfc = wappdb.Column(wappdb.String, primary_key=True)
    nombre = wappdb.Column(wappdb.String)
    situacion = wappdb.Column(wappdb.String)
    numofi_presuncion = wappdb.Column(wappdb.String)
    fechaofi_presuncion = wappdb.Column(wappdb.DateTime)
    numofi_desvirtuado = wappdb.Column(wappdb.String)
    fechaofi_desvirtuado = wappdb.Column(wappdb.DateTime)
    numofi_definitivo = wappdb.Column(wappdb.String)
    fechaofi_definitivo = wappdb.Column(wappdb.DateTime)
    numofi_sentfav = wappdb.Column(wappdb.String)
    fechaofi_sentfav = wappdb.Column(wappdb.DateTime)
