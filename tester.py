
import filecmp
import os
import sys
from os import listdir
from os.path import isfile, join

C_FILE_DIR       = "./test_files/"
EXPECTED_MIPS    = "./test_files/expected_MIPS/"
EXPECTED_LLVM    = "./test_files/expected_LLVM/"
EXPECTED_ERROR   = "./test_files/expected_ERROR/"
TEMP_DIR         = "./test_files/temp/"
COMMAND_MIPS     = "python3 c2mips.py"
COMMAND_LLVM     = "python3 c2llvm.py"
COMPILER_OUT_DIR = "./output/"

def compare_output(expected_file, test_file):

    # shallow = False to compare contents.
    return filecmp.cmp(expected_file, test_file, shallow=False)


def test_error(c_file, expected_file):
    """
        Compile the specified c-file to MIPS. The errors and warnings produced by the compiler will be checked.
    :param c_file: Path to the C-file that will be used for the test.
    :param expected_file: The file that contains the expected output.
    :return: True if the test succeeded, False if the test failed.
    """

    os.system("{} {} test.asm > {}".format(COMMAND_MIPS, c_file, TEMP_DIR + "test.txt"))

    return compare_output(expected_file, TEMP_DIR + "test.txt")


def test_mips(c_file, expected_file):
    """
        Compile the specified c-file to MIPS and run with MARS.
    :param c_file: Path to the C-file that will be used for the test.
    :param test_name: The name of the test. The temporary output will be named "test.asm" and "test.txt"
    :param expected_file: The file that contains the expected output.
    """

    os.system("{} {} test.asm > /dev/null".format(COMMAND_MIPS, c_file))
    os.system("java -jar Mars4_5.jar {} > {}".format(COMPILER_OUT_DIR + "test.asm", TEMP_DIR + "test.txt"))

    return compare_output(expected_file, TEMP_DIR + "test.txt")

def test_llvm(c_file, expected_file):
    """
        Compile the specified c-file to LLVM and run with LLI.
    :param c_file: Path to the C-file that will be used for the test.
    :param test_name: The name of the test. The temporary output will be named "test.ll" and "test.txt"
    :param expected_file: The file that contains the expected output.
    """

    os.system("{} {} test.ll > /dev/null".format(COMMAND_LLVM, c_file))
    os.system("lli {} > {}".format(COMPILER_OUT_DIR + "test.ll", TEMP_DIR + "test.txt"))

    return compare_output(expected_file, TEMP_DIR + "test.txt")

def get_test_names():
    error_warnings_tests = list()
    llvm_success_tests = list()
    mips_success_tests = list()
    files = [f for f in listdir(C_FILE_DIR) if isfile(join(C_FILE_DIR, f))]
    for file in files:
        if "SUCCESS" in file:
            test_name = "TEST_{}_{}".format("LLVM", file[:-2].upper())
            llvm_success_tests.append([test_name, file, file[:-2] + ".txt"])

            test_name = "TEST_{}_{}".format("MIPS", file[:-2].upper())
            mips_success_tests.append([test_name, file, file[:-2] + ".txt"])

        elif "WARNING" in file or "ERROR" in file:
            test_name = "TEST_{}".format(file[:-2].upper())
            error_warnings_tests.append([test_name, file, file[:-2] + ".txt"])
        else:
            # ignore demo files
            continue

    return llvm_success_tests, mips_success_tests, error_warnings_tests


def test_error_warning_all(test_list):

    print("=== ERROR/WARNING TESTS ===")
    run_testlist(test_list, test_error, EXPECTED_ERROR)


def test_mips_all(test_list):

    print("=== MIPS TESTS ===")
    run_testlist(test_list, test_mips, EXPECTED_MIPS)


def test_llvm_all(test_list):
    tests = get_test_names()[0]

    print("=== LLVM TESTS ===")
    run_testlist(tests, test_llvm, EXPECTED_LLVM)


def run_testlist(test_list, function, expected_dir):
    passed = True

    for test in test_list:
        testname    = test[0]
        c_filename  = test[1]
        ex_filename = test[2]


        result = function(C_FILE_DIR + c_filename, expected_dir + ex_filename)

        result_text = "PASSED" if result else "FAILED"

        if not result:
            passed = False

        print("[{}] {}".format(result_text, testname))

    passed_text = "passed" if result else "failed"

    print("[TOTAL] {}.".format(passed_text))


def main(args):

    # create test dir
    os.makedirs(TEMP_DIR, exist_ok=True)

    llvm_success_tests, mips_success_tests, error_warnings_tests = get_test_names()

    test_error_warning_all(error_warnings_tests)
    test_mips_all(mips_success_tests)
    test_llvm_all(llvm_success_tests)


if __name__ == "__main__":
    main(sys.argv)



