def parse_key_vector(key_value: str) -> list:
    if key_value.startswith("0x"):
        key_value = key_value[2:]  
    
    key = list()
    i = 0
    while i < len(key_value):
        key.append(
            int(key_value[i], 16) * 16
            + int(key_value[i+1], 16)
        )
        i += 2
        
    return key

def initialize_state_vector(size: int) -> list:
    state_vector = list()
    
    for i in range(size):
        state_vector.append(i)
        
    return state_vector

def swap(vector: list, source: int, dest: int) -> list:
    temp = vector[dest]
    vector[dest] = vector[source]
    vector[source] = temp
    
    return vector

def ksa(key_value: str, vectorlen: int = 256) -> list:
    key = parse_key_vector(key_value)
    state_vector = initialize_state_vector(vectorlen // 8)    
    
    keylen = len(key)
    svlen = len(state_vector)
    
    j = 0
    for i in range(vectorlen // 8):
        j = (j + state_vector[i] + key[i % keylen]) % svlen
        swap(state_vector, i, j)
    
    print(state_vector)
    return state_vector
    
def prga(input: str, state_vector: list) -> str:
    text = list()
    vec = list(reversed(input))
    i = 0
    j = 0
    svlen = len(state_vector)
    
    while len(vec):
        i = (i + 1) % svlen
        j = (j + state_vector[i]) % svlen
        swap(state_vector, i, j)
        
        k = state_vector[(state_vector[i] + state_vector[j]) % svlen]
        c = vec.pop()
        text.append(chr(ord(c) ^ k))
                
    return "".join(list(text))

def rc4(input: str, key_value: str, vectorlen: int = 256) -> str:
    state_vector = ksa(key_value, vectorlen)
    encrypted = prga(input, state_vector)
    return encrypted

if __name__ == "__main__":
    text = input("text to encrypt: ")
    key_value = input("key value (hex): ") .lower()
    vectorlen = int(input("vector length (bits): "))
    
    assert vectorlen % 8 == 0
    if not (text.startswith("\"") and text.endswith("\"")):
        # numerical value, not ascii text
        # todo this idc
        pass
        
    print(f"RC4(\"{text}\"): {rc4(text, key_value, vectorlen)}")