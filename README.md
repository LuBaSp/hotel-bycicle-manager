# Bicycle Management System

This application provides a graphical interface for managing bicycle bookings at a hotel. Built with the `customtkinter` library, it allows users to view and manage bicycle availability and bookings. The application supports viewing details of bookings, adding new ones, and clearing all bookings.

## Features

- **Real-time Booking Management:** Easily view and manage bookings with real-time updates on bicycle availability.
- **Color-Coded Status:** Bicycles are color-coded based on their availability:
  - **Available:** Green
  - **Occupied:** Red
  - **Booked for Over 10 Hours:** Yellow
- **Booking Details:** View and update booking details, including name, surname, and room number.
- **Clear All Bookings:** Clear all current bookings with a single button click.
- **Data Persistence:** Booking data is saved to and loaded from a JSON file.

## Prerequisites

- Python 3.x
- `customtkinter` library
- `tkinter` library (standard in Python)

## Installation

1. Clone or download the repository.
2. Install the required Python library if you haven't already:

    ```bash
    pip install customtkinter
    ```

## Usage

1. **Run the Application:**

    ```bash
    python Hotel_Bicycle_Manager.py
    ```

2. **Main Window:**
   - The main window displays the bicycle management interface with sections for different types of bicycles.
   - Each bicycle button is color-coded to indicate its availability.

3. **Booking Management:**
   - Click a bicycle button to open a details window.
   - In the details window, you can view or enter booking details and confirm or delete a booking.

4. **Clearing All Bookings:**
   - Click the "CLEAR ALL BOOKINGS" button to remove all existing bookings.

5. **Application Shutdown:**
   - The application automatically saves booking data when closed.

## Customization

- **Colors:** Modify the color constants at the top of the script to customize the appearance.
- **Button Names:** Adjust the `button_names` list to change the labels of the bicycle buttons.
- **Timer:** The `timer` variable defines the duration after which an occupied button changes color to yellow. Adjust this value as needed.

## Contributing

Feel free to contribute to the project by submitting issues or pull requests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Acknowledgements

- **customtkinter**: A library that simplifies the creation of modern, custom-styled Tkinter widgets.
- **Tkinter**: The standard GUI toolkit for Python.

## Contact

For questions or support, please contact luca.bachetti.spurio@gmail.com
