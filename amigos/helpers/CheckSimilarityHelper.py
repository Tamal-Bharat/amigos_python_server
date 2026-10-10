import os
import cv2
from helpers.DatabaseHelper import DatabaseHelper
from models.RegisterFaceModel import OperationMessageModel, RegisterFaceModel
from insightface.app import FaceAnalysis
from utilities.Constants import Constants
from utilities.LogFile import LogFile
from utilities.DateTimeUtil import DateTimeUtil

class CheckSimilarityHelper():

    #InsightFace Initialization
    app = FaceAnalysis(name="buffalo_l")
    app.prepare(ctx_id=-1)      # CPU

    databaseHelper = DatabaseHelper()
    AppConstants = Constants()
    AppLogFile = LogFile()
    dateTimeUtil = DateTimeUtil()

    def checkSimilarity(self)-> RegisterFaceModel | None:

        try:

            image_path = os.path.join(self.AppConstants.IMAGE_FRAME_FOLDER, self.AppConstants.IMAGE_FRAME_NAME)
            image = cv2.imread(image_path)

            if image is None:
                raise Exception("Could not read image") 

            else:                
                faces = self.app.get(image)

                if not faces:
                    raise Exception("No face detected")

                else:              
                    
                    if len(faces) != 1:
                        raise Exception("Multiple faces detected")

                    else:                      
                        # Liveliness check start here

                        # Extract face embedding
                            embedding = faces[0].embedding

                            results = self.databaseHelper.checkFaceSimilarity(embedding)

                            if results is None:
                                self.AppLogFile.writeAttandanceLogs("No face registered in database")

                            else:
                                highestSimilarity:int = 0;

                                employeeDetails = {
                                    "emp_id": "",
                                    "emp_name": "",
                                    "currentDateTime": ""
                                }

                                for erp_id, emp_name, distance in results:
                                    #similarity = (1 - distance) * 100
                                    similarity = int((1 - distance) * 100)

                                    if similarity > highestSimilarity:
                                        highestSimilarity = similarity
                                        employeeDetails['emp_id'] = erp_id
                                        employeeDetails['emp_name'] = emp_name
                                        employeeDetails['currentDateTime'] = self.dateTimeUtil.getCurrentDateTime()

                                    print(f"{erp_id} | {emp_name} | Similarity: {similarity:.2f}%")

                                print(str(employeeDetails))

                                if highestSimilarity > 50:   

                                    currentDate = self.dateTimeUtil.getCurrentDate()
                                    currentTime = self.dateTimeUtil.getCurrentTime()
                                    saveAttendanceStatus = self.databaseHelper.saveAttendance(employeeDetails['emp_id'], employeeDetails['emp_name'], currentDate, currentTime)     

                                    if saveAttendanceStatus is None:
                                        registerFaceModel = RegisterFaceModel(
                                            code=200,
                                            message = OperationMessageModel(
                                                opCode="F",
                                                opMessage= "Attendane not saved"
                                            )
                                        )

                                    else:                                       
                                        registerFaceModel = RegisterFaceModel(
                                            code=200,
                                            message = OperationMessageModel(
                                                opCode="S",
                                                opMessage=f"{employeeDetails}"
                                            )
                                        )

                                else:
                                    registerFaceModel = RegisterFaceModel(
                                        code=200,
                                        message = OperationMessageModel(
                                            opCode="F",
                                            opMessage="Employee not registered yet"
                                        )
                                    )

                                return registerFaceModel


        except Exception as e:
            self.AppLogFile.writeAttandanceLogs(str(e))
            return None