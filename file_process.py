def get_data(path: str):

    data_dict = {}

    with open(path, 'r') as file:
        for line in file:
            # Elimina los espacios en blanco y las comillas alrededor de las claves y valores
            line = line.strip().replace('"', '')

            # Divide la línea en la clave y el valor
            key, value = line.split(': ', 1)

            # Agrega la clave y el valor al diccionario
            data_dict[key] = value

    return data_dict
