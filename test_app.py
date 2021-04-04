from app import gender_encoder,survived_endr,clsfy_abst,pred

#data for testing the model output
dta = {'Pclass':3,'Sex':0,'Age':29,'Sibsp':1,'Parch':0,'Fare':35}

#testing gender_encoder 
def test_gender_encoder():
    assert 0 == gender_encoder(sex='FeMale')

#testing model output
def test_pred():
    assert 'Yes' == pred(dta)

