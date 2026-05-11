a= ["hello","hi"]
def len_dict(a):
        for b in a:
            length= len(b)
            if length  in final_dict:
                final_dict[length] += 1
            else:
                final_dict[length] = 1
        print(final_dict)
final_dict={}
len_dict(a)
# words = ["hi", "hello", "hey"]
# def length_dict(words):
#     for word in words:
#         length = len(word)
#         if length in leng_dict:
#             leng_dict[length] += 1
#         else:
#             leng_dict[length] = 1
# leng_dict = {}

# length_dict(words)
# print(leng_dict)