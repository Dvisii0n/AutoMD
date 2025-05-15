import csv


class csv_format_tool():
    def __init__(self):
        pass

    def upload_csv(self, file_path: str) -> dict:
        template = {}
        with open(file_path) as csvfile:
            content = csv.reader(csvfile, delimiter=",")

            for row in content:
                area_num = row[0]
                area_name = row[1]
                area_type = "COMUN" 
                if row[2] != "AC":
                    area_type = "PRIVATIVA"

                template[int(row[0])] = f"AREA {area_type} ({area_num}) {area_name}\nDESCRIPCION:\nAL NORESTE:\nAL SURESTE:\nAL ORIENTE:\nAL PONIENTE:\n \n"
        with open("template.txt", "w") as t:
            for desc in template:
                t.write(template[desc])
            print("Created template.txt")
                
        return template
        
                
            
        

                

    



