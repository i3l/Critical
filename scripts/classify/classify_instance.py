import subprocess

test_file = "temp.arff"
model_file = "../../data/weka_models/j48_full.model"
weka_jar = "weka-3-6-10/weka.jar"

header = """
@RELATION icu
@ATTRIBUTE 'var_Albumin' REAL
@ATTRIBUTE 'var_ALP' REAL
@ATTRIBUTE 'var_ALT' REAL
@ATTRIBUTE 'var_AST' REAL
@ATTRIBUTE 'var_Bilirubin' REAL
@ATTRIBUTE 'var_BUN' REAL
@ATTRIBUTE 'var_Cholesterol' REAL
@ATTRIBUTE 'var_Creatinine' REAL
@ATTRIBUTE 'var_DiasABP' REAL
@ATTRIBUTE 'var_FiO2' REAL
@ATTRIBUTE 'var_GCS' REAL
@ATTRIBUTE 'var_Glucose' REAL
@ATTRIBUTE 'var_HCO3' REAL
@ATTRIBUTE 'var_HCT' REAL
@ATTRIBUTE 'var_HR' REAL
@ATTRIBUTE 'var_K' REAL
@ATTRIBUTE 'var_Lactate' REAL
@ATTRIBUTE 'var_Mg' REAL
@ATTRIBUTE 'var_MAP' REAL
@ATTRIBUTE 'var_Na' REAL
@ATTRIBUTE 'var_NIDiasABP' REAL
@ATTRIBUTE 'var_NIMAP' REAL
@ATTRIBUTE 'var_NISysABP' REAL
@ATTRIBUTE 'var_PaCO2' REAL
@ATTRIBUTE 'var_PaO2' REAL
@ATTRIBUTE 'var_pH' REAL
@ATTRIBUTE 'var_Platelets' REAL
@ATTRIBUTE 'var_RespRate' REAL
@ATTRIBUTE 'var_SaO2' REAL
@ATTRIBUTE 'var_SysABP' REAL
@ATTRIBUTE 'var_Temp' REAL
@ATTRIBUTE 'var_TropI' REAL
@ATTRIBUTE 'var_TropT' REAL
@ATTRIBUTE 'var_Urine' REAL
@ATTRIBUTE 'var_WBC' REAL
@ATTRIBUTE 'var_Weight' REAL
@ATTRIBUTE 'abnorm_Albumin' REAL
@ATTRIBUTE 'abnorm_ALP' REAL
@ATTRIBUTE 'abnorm_ALT' REAL
@ATTRIBUTE 'abnorm_AST' REAL
@ATTRIBUTE 'abnorm_Bilirubin' REAL
@ATTRIBUTE 'abnorm_BUN' REAL
@ATTRIBUTE 'abnorm_Cholesterol' REAL
@ATTRIBUTE 'abnorm_Creatinine' REAL
@ATTRIBUTE 'abnorm_DiasABP' REAL
@ATTRIBUTE 'abnorm_FiO2' REAL
@ATTRIBUTE 'abnorm_GCS' REAL
@ATTRIBUTE 'abnorm_Glucose' REAL
@ATTRIBUTE 'abnorm_HCO3' REAL
@ATTRIBUTE 'abnorm_HCT' REAL
@ATTRIBUTE 'abnorm_HR' REAL
@ATTRIBUTE 'abnorm_K' REAL
@ATTRIBUTE 'abnorm_Lactate' REAL
@ATTRIBUTE 'abnorm_Mg' REAL
@ATTRIBUTE 'abnorm_MAP' REAL
@ATTRIBUTE 'abnorm_Na' REAL
@ATTRIBUTE 'abnorm_NIDiasABP' REAL
@ATTRIBUTE 'abnorm_NIMAP' REAL
@ATTRIBUTE 'abnorm_NISysABP' REAL
@ATTRIBUTE 'abnorm_PaCO2' REAL
@ATTRIBUTE 'abnorm_PaO2' REAL
@ATTRIBUTE 'abnorm_pH' REAL
@ATTRIBUTE 'abnorm_Platelets' REAL
@ATTRIBUTE 'abnorm_RespRate' REAL
@ATTRIBUTE 'abnorm_SaO2' REAL
@ATTRIBUTE 'abnorm_SysABP' REAL
@ATTRIBUTE 'abnorm_Temp' REAL
@ATTRIBUTE 'abnorm_TropI' REAL
@ATTRIBUTE 'abnorm_TropT' REAL
@ATTRIBUTE 'abnorm_Urine' REAL
@ATTRIBUTE 'abnorm_WBC' REAL
@ATTRIBUTE 'abnorm_Weight' REAL
@ATTRIBUTE 'MechVent' {0, 1}
@ATTRIBUTE 'SAPS-1' REAL
@ATTRIBUTE 'SOFA' REAL
@ATTRIBUTE 'Death' {0, 1}
@DATA
"""

def test():
	print classify('5.5225,1089,841,3844,0.55502,2741.2,?,0.0185,961.65,0.13065,18.846,754.2,53.45,46.19,234.01,0.1025,0.14625,4.589,723.23,5,1640.9,1322.7,275.6,114.93,5377.7,0.020093,41500,?,3.05,702.82,0.195,?,?,6434.4,171.77,0,1,0,1,1,0,1,?,0,1,0,0,1,0.8,1,0.20548,0,0.125,1,0.73333,0,1,0.93023,0.23256,0.86667,0.8,0.66667,1,?,0.2,0.71667,0.13889,?,?,?,1,?,1,19,8'.split(','))
	print classify('?,?,?,?,?,512.25,?,0.0275,47.6,0.0441,62.217,444.25,35.25,71.443,517.66,0.0525,0.084,3.3456,91.325,98.25,16.25,79.606,206.25,32.5,8676.6,0.0036333,11957,?,1.5833,152.1,1.7476,?,?,501000,38.533,0,?,?,?,?,?,0.75,?,0,0.125,0,0,1,0.75,0.75,0.42553,0,0,1,0,1,0,0,0.36364,0.33333,1,0.83333,0,?,0,0.25,0.7619,?,?,?,0.25,?,1,16,4'.split(','))

def run_command(command):
    return subprocess.check_output(command, shell=True)

# Call weka on the instance and extract the classifaction.
def classify(value_list):
	instance = ','.join(value_list) + ',?'
	with open(test_file, 'w') as the_file:
		the_file.write(header)
		the_file.write(instance)
	weka_command = "java -classpath " + weka_jar + " weka.classifiers.trees.J48 -T " + test_file + " -l " + model_file + " -p 1"
	result = run_command(weka_command)
	try:
		return str(result.split(':')[2][0])
	except Exception:
		return '?'
	