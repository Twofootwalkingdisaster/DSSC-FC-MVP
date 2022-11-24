import pandas as pd
import dssc_fc_mvp_storage as storage_information


# This function is used for updating the stock information every day
def update_stock_data_daily():
    company_list = {'Alphabet': 'GOOG', 'Apple': 'AAPL', 'BMO': 'BMO.TO', 'Cisco': 'CSCO', 'IBM': 'IBM', 'Meta': 'META',
                    'Microsoft': 'MSFT', 'Nvidia': 'NVDA', 'Oracle': 'ORCL', 'RBC': 'RY.TO', 'Scotia': 'BNS.TO',
                    'TSM': 'TSM',
                    'TXN': 'TXN', 'VZ': 'VZ'}

    for company_name, company_stock_name in company_list.items():
        # The code below updates all the files with the latest stock data till date
        update_file = file_name = None
        company_name = storage_information.S3DatabaseActions.update_files_to_latest_data(company_name,
                                                                                         company_stock_name)

    storage_information.Create_Local_Files.change_dir_for_upload()
    storage_information.S3DatabaseActions.update_s3_database()
    storage_information.Create_Local_Files.remove_local_data_set_files()


# The main start point of the project is this function
def main():
    storage_information.Create_Local_Files.create_local_file()
    storage_information.InitializeDSSCService.initialize_dssc_service()
    update_stock_data_daily()


# START POINT OF THE PROGRAM
if __name__ == "__main__":
    main()




