import pandas as pd
import dssc_fc_mvp_storage as storage_information


# The main start point of the project is this function
def main():
    storage_information.Create_Local_Files.create_local_file()
    storage_information.InitializeDSSCService.initialize_dssc_service()
    company_list = ()

    # The code below updates all the files with the latest stock data till date
    update_file, file_name = storage_information.S3DatabaseActions.update_files_to_latest_data("BMO")
    storage_information.S3DatabaseActions.update_s3_database(update_file, file_name)


# START POINT OF THE PROGRAM
if __name__ == "__main__":
    main()




