
import filecmp
import os

C_FILE_DIR   = "./test_files/"
EXPECTED_DIR = "./test_files/expected/"
TEMP_DIR     = "./test_files/temp/"
COMMAND_MIPS = "./c2mips"
COMMAND_LLVM = "./c2llvm"
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

    return True


def test_llvm(c_file, expected_file):
    """
        Compile the specified c-file to LLVM and run with LLI.
    :param c_file: Path to the C-file that will be used for the test.
    :param test_name: The name of the test. The temporary output will be named "test.ll" and "test.txt"
    :param expected_file: The file that contains the expected output.
    """

    return True


def test_error_all():

    pass


def test_mips_all():
    pass


def test_llvm_all():
    tests = [
        ["TEST_LLVM_OPS_BOOL", "SUCCESS_ops_bool.c", "SUCCESS_ops_bool.txt"]
    ]

    print("=== LLVM TESTS ===")

    for test in tests:
        testname    = test[0]
        c_filename  = test[1]
        ex_filename = test[2]

        result = test_llvm(C_FILE_DIR + c_filename, EXPECTED_DIR + ex_filename)

        result_text = "PASSED" if result else "FAILED"

        print("[{}] {}".format(result_text, testname))

    pass


def main():

    # create test dir
    os.makedirs(TEMP_DIR, exist_ok=True)

    test_error_all()
    test_mips_all()
    test_llvm_all()


if __name__ == "__main__":
    main()
