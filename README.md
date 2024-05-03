# Social Media App
## Installation Guide

### Linux
1.Cài đặt python : sudo apt-get install python ```bash
2.Cài đặt django : pip install django
3.Di chuyển vào thư mục dự án : cd đường dẫn đến dự án /social_media_app
4.Cài đặt các thư viện cần thiết từ file requirements.txt : pip install -r requirements.txt
5.Chạy dự án web : python manage.py runserver

### Windows
1.Cài đặt python
    1.Truy cập vào trang web của [python](https://www.python.org/downloads/) để lựa chọn phiên bản phù hợp
    2.Chạy file .exe để cài đặt
    3.Kiểm tra phiên bản : python --version
2.Cài đặt django : pip install django
3.Di chuyển vào thư mục dự án : cd đường dẫn đến dự án /social_media_app
4.Cài đặt các thư viện cần thiết từ file requirements.txt : pip install -r requirements.txt
5.Chạy dự án web : python manage.py runserver




# website_to_register_to_buy_movie_tickets
# PROJECT WEBSITE PROGRAMING - ASP.NET MVC - YEAR 3

Name of the project: *Website xem phim Twoone*

## Abstract
- Website watching movie Twoone with up to **4000 films** and many interesting functions. We use asp.net MVC 5 technology to build the website. 
  The website has some layouts look like this:

- Here is short demo about Twoone website. [Click here to see full!!!](https://www.youtube.com/watch?v=pwxriq0qSIQ)

  <video src="source\short demo.mp4" style="zoom:50%;"></video>
## Idea

### Objects use

- User: watch movie, comment, update premium edit profile, register, login, forgot password, search.
- Admin: 
    - Management: film, director, actor, hashtags, genres, licenses.
    - Statistic: revenue month, revenue year, user subscribe month, user subscribe year, number of subscribers.

### Entity relationship diagram(ERD)

<img src="website_to_register_to_buy_movie_tickets\source\ERD.png" style="zoom:60%;" alt ="ERD"/>

### Use case summary

<img src="website_to_register_to_buy_movie_tickets\source\Usecasetq.png" style="zoom:60%" alt="usecase" />

## Requirements
- C# 
- Entity Framework (code first)
- Asp.net MCV 5
- Other library: pagelist, md5, mail, jquery, bootstrap
## Database (MSSQL)

### Diagram

<img src="website_to_register_to_buy_movie_tickets\source\sql.png" style="zoom:60%;" alt="sql diagram"/>

You can see more at full report in source folder or 

[**Click here!!!**]: source/fullreport.pdf	"Click here!!!"



#### Interface and Function of website

##### Home page

##### Login & Register & Reset Password

| Login                                                        | Register                                                     | Reset password                                               |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| <img src="website_to_register_to_buy_movie_tickets\source\login.png" alt="login" style="zoom:80%;" /> | <img src="website_to_register_to_buy_movie_tickets\source\register.png" alt="register" style="zoom:80%;" /> | <img src="website_to_register_to_buy_movie_tickets\source\twoonez-001-site1.itempurl.com_User_ForgotPassword_class=small.png" alt="twoonez-001-site1.itempurl.com_User_ForgotPassword_class=small" style="zoom:80%;" /> |

##### List film & actor

| List film - type list                                                                                                                                                          | List film - type grid                                                                                                                   | List actor                                                                                                                    |
|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------|
| <img src="website_to_register_to_buy_movie_tickets\source\twoonez-001-site1.itempurl.com_Movie_SearchByFilter_Grid=False.png" alt="twoonez-001-site1.itempurl.com_Movie_SearchByFilter_Grid=False" style="zoom:50%;" /> | <img src="website_to_register_to_buy_movie_tickets\source\twoonez-001-site1.itempurl.com_Movie_SearchByFilter.png" alt="twoonez-001-site1.itempurl.com_Movie_SearchByFilter"  /> | <img src="website_to_register_to_buy_movie_tickets\source\twoonez-001-site1.itempurl.com_Movie_ActorGrid.png" alt="twoonez-001-site1.itempurl.com_Movie_ActorGrid"  /> |

#### Movie Details

| film information                                             | similar film                                                 |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| <img src="website_to_register_to_buy_movie_tickets\source\twoonez-001-site1.itempurl.com_Movie_MovieDetail_3262.png" alt="twoonez-001-site1.itempurl.com_Movie_MovieDetail_3262" style="zoom:80%;" /> | <img src="website_to_register_to_buy_movie_tickets\source\twoonez-001-site1.itempurl.com_Movie_MovieDetail_3262 (2).png" alt="twoonez-001-site1.itempurl.com_Movie_MovieDetail_3262 (2)" style="zoom:80%;" /> |

##### Watching movie

##### <img src="website_to_register_to_buy_movie_tickets\source\twoonez-001-site1.itempurl.com_Movie_WatchingMovie_3262.png" alt="twoonez-001-site1.itempurl.com_Movie_WatchingMovie_3262" style="zoom: 50%;" />

#### Premium

| Type of service                                              | type of payment                                              |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| <img src="website_to_register_to_buy_movie_tickets\source\twoonez-001-site1.itempurl.com_Payment_PaymentPage.png" alt="twoonez-001-site1.itempurl.com_Payment_PaymentPage" style="zoom:80%;" /> | <img src="website_to_register_to_buy_movie_tickets\source\twoonez-001-site1.itempurl.com_Payment_ChonPhuongThucThanhToan_1.png" alt="twoonez-001-site1.itempurl.com_Payment_ChonPhuongThucThanhToan_1" style="zoom:80%;" /> |


#### User

| uSER PROFILE                                                 | FILM RATED                                                   | CHANGE PASS                                                  |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| <img src="website_to_register_to_buy_movie_tickets\source\twoonez-001-site1.itempurl.com_User_ShowInfor.png" alt="twoonez-001-site1.itempurl.com_User_ShowInfor" style="zoom:80%;" /> | <img src="website_to_register_to_buy_movie_tickets\source\twoonez-001-site1.itempurl.com_User_ShowInfor_mode=favorite.png" alt="twoonez-001-site1.itempurl.com_User_ShowInfor_mode=favorite" style="zoom:80%;" /> | <img src="website_to_register_to_buy_movie_tickets\source\twoonez-001-site1.itempurl.com_User_ShowInfor_mode=changepass.png" alt="twoonez-001-site1.itempurl.com_User_ShowInfor_mode=changepass" style="zoom:80%;" /> |

##### Admin

| Login                                                        | Forget password                                              |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| <img src="website_to_register_to_buy_movie_tickets\source\twoonez-001-site1.itempurl.com_Administrator_Adm_TrangChu_Login.png" alt="twoonez-001-site1.itempurl.com_Administrator_Adm_TrangChu_Login" style="zoom:80%;" /> | <img src="website_to_register_to_buy_movie_tickets\source\twoonez-001-site1.itempurl.com_Administrator_Adm_TrangChu_ForgotPassword.png" alt="twoonez-001-site1.itempurl.com_Administrator_Adm_TrangChu_ForgotPassword" style="zoom:80%;" /> |

##### Home Page Admin

<img src="website_to_register_to_buy_movie_tickets\source\twoonez-001-site1.itempurl.com_Administrator_Adm_TrangChu_Adm_Home.png" alt="twoonez-001-site1.itempurl.com_Administrator_Adm_TrangChu_Adm_Home" style="zoom:80%;" />

##### 8 function management (C-R-U-D)

example: Film Management

| List film                                                    | Delete                                                       | Create                                                       | Edit                                                         |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| <img src="website_to_register_to_buy_movie_tickets\source\twoonez-001-site1.itempurl.com_Administrator_Adm_Phim.png" alt="twoonez-001-site1.itempurl.com_Administrator_Adm_Phim" style="zoom:80%;" /> | <img src="website_to_register_to_buy_movie_tickets\source\twoonez-001-site1.itempurl.com_Administrator_Adm_Phim_Delete_3262.png" alt="twoonez-001-site1.itempurl.com_Administrator_Adm_Phim_Delete_3262" style="zoom:80%;" /> | <img src="website_to_register_to_buy_movie_tickets\source\twoonez-001-site1.itempurl.com_Administrator_Adm_Phim_Create.png" alt="twoonez-001-site1.itempurl.com_Administrator_Adm_Phim_Create" style="zoom:80%;" /> | <img src="website_to_register_to_buy_movie_tickets\source\twoonez-001-site1.itempurl.com_Administrator_Adm_Phim_Edit_3262.png" alt="twoonez-001-site1.itempurl.com_Administrator_Adm_Phim_Edit_3262" style="zoom:80%;" /> |

#### Statical

<img src="website_to_register_to_buy_movie_tickets\source\twoonez-001-site1.itempurl.com_Administrator_Adm_TrangChu_Statistical.png" alt="twoonez-001-site1.itempurl.com_Administrator_Adm_TrangChu_Statistical" style="zoom:50%;" />

Above is all of function we made

#### Any question you can contact with us

#### Contact email:
- [letanminhtoan2505@gmail.com](mailto:letanminhtoan2505@gmail.com)
- [lengocgiau2k3@gmail.com](mailto:lengocgiau2k3@gmail.com)
- [dominhquan15623@gmail.com](mailto:dominhquan15623@gmail.com)
- [tangquoctuan2003@gmail.com](mailto:tangquoctuan2003@gmail.com)


Author:

| leader                | member       | member         | member         |
|-----------------------|--------------|----------------|----------------|
|Lê Tấn Minh Toàn       | Lê Ngọc Giàu | Đỗ Minh Quân   | Tăng QUốc Tuấn |

#### Note:
The website won second prize at the University of Natural Sciences in the Hackathon Contest

