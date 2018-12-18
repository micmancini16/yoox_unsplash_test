class Viewer:
    def print_json(self, json):
        raise NotImplementedError

class JSON_Viewer(Viewer):
    def print_photo_description(self, img_dict):
        print("ID:{}".format(img_dict['id']))
        print("Description: {}".format(img_dict['description']))
        print("Size: {} x {}".format(img_dict['width'],img_dict['height']))
        print("Number of likes: {}".format(img_dict['likes']))

    def print_json(self, json):
        for i, img in enumerate(json):
            print("*****************")
            print("Result {} out of {}:".format(i+1,len(json)))
            self.print_photo_description(img)

