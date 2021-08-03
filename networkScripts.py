#PRUEBA DE CONCEPTO PARA OBTENER EL GATEWAY
import netifaces


def get_default_gateway_ip():
    """Return the default gateway IP."""
    gateways = netifaces.gateways()
    defaults = gateways.get("default")

    if not defaults:
        print("No hay GW")
        return

    gw_info=defaults.get(netifaces.AF_INET)
    print(gw_info[0])



