from webapp.CFDImodels import CFDI, Aerolineas, AerolineasOtrosCargos, Receptor


def cfdiscompl(cual):
    comps = ('Donatarias', 'LeyendasFiscales', 'Complemento_SPEI', 'ValesDeDespensa', 'EstadoDeCuentaCombustible',
             'ConsumoDeCombustibles', 'Divisas', 'PFIntegranteCoordinado', 'TuristaPasajeroExtranjero', 'PagoEnEspecie',
             'CFDIRegistroFiscal', 'INE', 'Aerolineas', 'obrasarteantiguedades', 'ImpuestosLocales', 'Vehiculousado',
             'NotariosPublicos', 'parcialesconstruccion', 'renovacionysustitucionvehiculos', 'certificadodedestruccion',
             'ComercioExterior', 'Pagos', 'Nomina')
    compsconc = ('compC_acreditamientoIEPS', 'compC_instEducativas', 'compC_VentaVehiculos',
                 'compC_PorCuentaDeTerceros')
    if cual in comps:
        if cual == 'Aerolineas':
            aero = CFDI.query.join(Receptor, CFDI.uuid == Receptor.uuid).add_columns(CFDI.uuid, CFDI.serie,
                                                                                     CFDI.folio, CFDI.fecha,
                                                                                     CFDI.subtotal, CFDI.total,
                                                                                     Receptor.RFC,
                                                                                     Receptor.nombre).join(Aerolineas,
                                                                                                           CFDI.uuid == Aerolineas.uuid).join(
                AerolineasOtrosCargos, Aerolineas.id == AerolineasOtrosCargos.id).add_columns(Aerolineas.TUA,
                                                                                              Aerolineas.TotalOtrosCargos,
                                                                                              AerolineasOtrosCargos.CodigoCargo,
                                                                                              AerolineasOtrosCargos.Importe).all()
            cfdi = ''
            cols = ['RFC', 'serie', 'folio', 'fecha',  'subtotal', 'total', 'TUA', 'Total Otros Cargos']
            resp = []
            line = None
            for c_f in aero:
                if cfdi != c_f[1]:
                    if line is not None:
                        resp.append(line)
                    line = [c_f[7], c_f[2], c_f[3], c_f[4], c_f[5], c_f[6], c_f[9], c_f[10]]
                    cfdi = c_f[1]
                    if c_f[11] not in cols:
                        cols.append(c_f[11])
                        line.append(c_f[12])
                else:
                    if c_f[11] not in cols:
                        cols.append(c_f[11])
                        line.append(c_f[12])
            if line is not None:
                resp.append(line)
            return resp, cols
