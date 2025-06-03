import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Definir las variables
ingreso = ctrl.Antecedent(np.arange(0, 20001, 1000), 'ingreso')
deuda = ctrl.Antecedent(np.arange(0, 10001, 500), 'deuda')
historial = ctrl.Antecedent(np.arange(0, 11, 1), 'historial')
riesgo = ctrl.Consequent(np.arange(0, 11, 1), 'riesgo')

# Funciones de membresía
ingreso['bajo'] = fuzz.trimf(ingreso.universe, [0, 0, 5000])
ingreso['medio'] = fuzz.trimf(ingreso.universe, [3000, 8000, 13000])
ingreso['alto'] = fuzz.trimf(ingreso.universe, [10000, 15000, 20000])

deuda['baja'] = fuzz.trimf(deuda.universe, [0, 0, 3000])
deuda['media'] = fuzz.trimf(deuda.universe, [2000, 5000, 7000])
deuda['alta'] = fuzz.trimf(deuda.universe, [6000, 8000, 10000])

historial['malo'] = fuzz.trimf(historial.universe, [0, 0, 3])
historial['regular'] = fuzz.trimf(historial.universe, [2, 5, 7])
historial['bueno'] = fuzz.trimf(historial.universe, [6, 8, 10])

riesgo['alto'] = fuzz.trimf(riesgo.universe, [7, 10, 10])
riesgo['medio'] = fuzz.trimf(riesgo.universe, [4, 5, 7])
riesgo['bajo'] = fuzz.trimf(riesgo.universe, [0, 0, 4])

# Reglas
rule1 = ctrl.Rule(ingreso['bajo'] & deuda['alta'] & historial['malo'], riesgo['alto'])
rule2 = ctrl.Rule(ingreso['medio'] & deuda['media'] & historial['regular'], riesgo['medio'])
rule3 = ctrl.Rule(ingreso['alto'] & deuda['baja'] & historial['bueno'], riesgo['bajo'])
rule4 = ctrl.Rule(ingreso['medio'] & deuda['baja'] & historial['bueno'], riesgo['bajo'])
rule5 = ctrl.Rule(ingreso['bajo'] & historial['bueno'], riesgo['medio'])

# Controlador
sistema_control = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5])
simulador = ctrl.ControlSystemSimulation(sistema_control)

# Función para evaluar
# En fuzzy_model.py, dentro de la función evaluar_riesgo
def evaluar_riesgo(ing, deu, his):
    simulador.input['ingreso'] = ing
    simulador.input['deuda'] = deu
    simulador.input['historial'] = his

    try:
        simulador.compute()
        resultado = simulador.output['riesgo']
    except ValueError: # skfuzzy puede lanzar ValueError si no puede computar
        # Si no se puede calcular, podrías asumir un riesgo medio o alto por defecto
        # o lanzar una excepción personalizada para un mejor manejo en la ruta de Flask
        print("Advertencia: No se pudo inferir un riesgo para las entradas dadas.")
        resultado = 5 # Un valor por defecto para 'riesgo' en caso de fallo
        # O podrías considerar un riesgo más cauteloso si no hay inferencia:
        # resultado = 8 # por ejemplo, para un riesgo 'alto' por defecto

    if resultado < 4:
        return 'Bajo'
    elif resultado < 7:
        return 'Medio'
    else:
        return 'Alto'
