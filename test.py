import unittest
from CBACObligationWPermissions import * 


class TestStringMethods(unittest.TestCase):

    def test_teacher_authorised(self):
        self.assertTrue(teacher.isAuthorised(READ, studentdata))
        self.assertTrue(teacher.isAuthorised(WRITE, studentdata))
        self.assertFalse(teacher.isAuthorised(READ, parentdata))
        self.assertFalse(teacher.isAuthorised(WRITE, parentdata))
    
    def test_categories(self):
        self.assertEqual(teacher.getAllCategories(), ["TEACHERS"])

    def test_permissions(self):
        self.assertEqual(teacher.getAllPermissions(), [STUDENTREADPERMMISSION, STUDENTWRITEPERMMISSION])
        self.assertNotEqual(teacher.getAllPermissions(), [STUDENTWRITEPERMMISSION])
        self.assertNotEqual(teacher.getAllPermissions(), [STUDENTREADPERMMISSION])

    def test_obligations(self):
        eventmanager = EventManager()
        eventmanager.addObligationPrincipal(obligation1)
        eventmanager.addObligationPrincipal(obligation2)
        self.assertEqual(eventmanager.checkObligations(teacher, READ, studentdata), obligation1)
        self.assertEqual(eventmanager.checkObligations(teacher, WRITE, parentdata), obligation2)
        self.assertFalse(eventmanager.checkObligations(teacher, READ, parentdata), False)
    
if __name__ == '__main__':
    unittest.main()