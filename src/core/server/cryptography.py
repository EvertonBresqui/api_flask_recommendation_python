import bcrypt

class Cryptography():

    def hash(value):
        hashed = ''
        if isinstance(value, str) == True:
            hashed = bcrypt.hashpw(value, bcrypt.gensalt())
        
        return hashed
    
    def compareHash(hashed, value):
        is_equal = False
        if isinstance(value, str) == True:
            is_equal = (bcrypt.hashpw(value, hashed) == hashed)

        return is_equal