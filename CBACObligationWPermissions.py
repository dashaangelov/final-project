
# Attributes: actionIdentifier
class Action:

    def __init__(self, actionIdentifier):
        self.actionIdentifier = actionIdentifier

# Attributes: name
class Resource:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

# Attributes: action, resource
class Permission:
    def __init__(self, name, action: Action, resource: Resource):
        self.name = name
        self.action = action
        self.resource = resource
    
    def __str__(self):
        return ("Permission to perform " + self.action.actionIdentifier + " on " + self.resource)

# Attributes: name, permissions
class Category:
    # A Category is a distinct classes or groups to which Entities may be assigned
    # 
    def __init__(self, name):
        self.name = name
        self.permissions = []
    
    def __str__(self):
        return self.name
    
    def add_permission(self, permission: Permission):
        self.permissions.append(permission)
    
    def remove_permission(self, permission: Permission):
        self.permissions.remove(permission)

# Attributes: name, Category
class Principal:

    def __init__(self, name):
        self.name = name
        self.categories = []
        self.temporalPermissions = []
    
    def add_category(self, category:Category):
        self.categories.append(category)

    def getAllCategories(self):
        results = []
        for category in self.categories:
            results.append(category.name)
        return results

    # Returns Permissions
    def getAllPermissions(self):
        result = []
        for category in self.categories:
            for permission in category.permissions:
                result.append(permission)
        for permission in self.temporalPermissions:
            result.append(permission)

        return result
    
    def getAllPermissionString(self):
        result = []
        for category in self.categories:
            for permission in category.permissions:
                result.append(permission.name)
        for permission in self.temporalPermissions:
            result.append(permission.name)

        return result
    
    def isAuthorised(self, action: Action, resource: Resource):
        permissions = self.getAllPermissions()
        # Check if this User has permission to access this resource
        for permission in permissions:
            permActionName = permission.action.actionIdentifier
            permResource = permission.resource.name

            if action.actionIdentifier == permActionName and resource.name == permResource:
                return True
        return False

    def __str__(self):
        return self.name
    
    def doAction(self, action: Action, resource: Resource):
        # Check if user is authorised to the actionIdentifier
        # Check the obligations for this resource
        
        if not self.isAuthorised(action, resource):
            print("Princiapl is not authorised to do " + str(action.actionIdentifier) + " on this resource")
            return False
        
        return True

import time
import datetime
import hashlib

class ObligationPrincipal:
    def __init__(self, action, resource, principal, ttl, temporalPermission = False, ge1 = "None", ge2 = "None"):
        self.ge1 = ge1
        self.ge2 = ge2
        self.action = action
        self.resource = resource
        self.principal = principal
        self.temporalPermission = temporalPermission
        self.ttl = ttl

    def getObligationActions(self):
        if self.ge1 is not None and self.ge2 is not None:
            return [self.ge1, self.ge2]
        elif self.ge1 is None and self.ge2 is not None:
            return [self.ge2]
        elif self.ge1 is not None and self.ge2 is None:
            return [self.ge1]
        else:
            return []

class EventManager:
    
    def __init__(self):
        self.obligationPrincipals = []
        self.eventHistory = []
        self.eventLog = []
        self.unfulfilledObligations = {}
        self.uncompletedObligations = []

    def addEvent(self, principal, action, resource):
        isAuthorised = principal.isAuthorised(action, resource)
        currentTime = str(datetime.datetime.now())
        currentEpochTime = time.time()
        performedPreviousObligationAction = False
        obligation = self.checkObligations(principal, action, resource)
        isAuthorised = principal.isAuthorised(action, resource)

        message = principal.name + action.actionIdentifier + resource.name
        encodedMessaged = message.encode()
        self.hash_value = hashlib.sha512(encodedMessaged).hexdigest()

        self.eventLog.append([currentTime, principal.name, action.actionIdentifier, resource.name])
        fufilledObligation = self.fulfilObligation(self.hash_value, currentEpochTime)

        if fufilledObligation == True:
            print("Fufilled Old Obligation")
            performedPreviousObligationAction = True

        if obligation is not False and isAuthorised:
            print("User is Authorised")
            self.eventHistory.append([currentTime, principal, action, resource, obligation])
            if performedPreviousObligationAction == False:
                self.addPostObligations(self.hash_value,obligation, currentEpochTime, principal, action, resource)
        elif obligation is not False and not isAuthorised:
            if obligation.temporalPermission is not False:
                print("User is not authorised but there is temporal permission")
                self.eventHistory.append([currentTime, principal, action, resource, obligation])
                if performedPreviousObligationAction == False:
                    self.addPostObligations(self.hash_value,obligation, currentEpochTime, principal, action, resource)
        elif isAuthorised:
            self.eventHistory.append([currentTime, principal, action, resource])
            print("User is authorised, No Obligation")
        else:
            print("NOT AUTHORSIED")
            pass
    
    def checkObligations(self, principal, action, resource):
        for obligation in self.obligationPrincipals:
            print(obligation.principal.name + obligation.action.actionIdentifier + obligation.resource.name)
            print(principal.name + action.actionIdentifier + resource.name)
            if obligation.action.actionIdentifier == action.actionIdentifier and obligation.resource.name == resource.name and obligation.principal.name == principal.name:
                print("done here")
                return obligation
        return False
    
    def addObligationPrincipal(self, obligation):
        self.obligationPrincipals.append(obligation)
    
    def addPostObligations(self, hash, obligation, currentEpochTime, principal, action, resource):
        if obligation.ge2 == "None":
            pass
            #print("[NO] GE2 Obligation to fulfil")
        else:
            self.unfulfilledObligations[hash] = {
                "timeout": currentEpochTime + obligation.ttl, 
                "ttl": obligation.ttl,
                "principal": principal,
                "action": action,
                "resource": resource}
    
    def fulfilObligation(self, hash_value, currentEpochTime):

        if hash_value in self.unfulfilledObligations.keys():
            if currentEpochTime < self.unfulfilledObligations[hash_value]["timeout"]:
                del self.unfulfilledObligations[hash_value]
                return True
            else:
                print("Temporal position has expired")
                self.uncompletedObligations.append("Temporal permission Expired at " +  str(self.unfulfilledObligations[hash_value]["timeout"])+ "\n")
                del self.unfulfilledObligations[hash_value]
                return False
        else:
            print("No obligation to fufill")
            return False


studentdata = Resource("Student Data")
parentdata = Resource("Parent Data")

# ACTIONS
READ = Action("READ")
WRITE = Action("WRITE")

# PERMISSION
STUDENTREADPERMMISSION = Permission("Read_Student_Data", READ, studentdata)
STUDENTWRITEPERMMISSION = Permission("Write_Student_Data", WRITE, studentdata)

# CATEGORIES
teachers = Category("TEACHERS")
teachers.add_permission(STUDENTREADPERMMISSION)
teachers.add_permission(STUDENTWRITEPERMMISSION)

# Principal
teacher = Principal("John Doe")

# Add Category to Teacher
teacher.add_category(teachers)

obligation1 = ObligationPrincipal(
    READ, studentdata, teacher, 
    temporalPermission=True, ttl=15, 
    ge1="", ge2="Write Parent Data")


obligation2 = ObligationPrincipal(WRITE, parentdata, teacher, temporalPermission=True,ttl=10, ge1="Send email to headmaster", ge2="Send letter on behalf of headmaster")
