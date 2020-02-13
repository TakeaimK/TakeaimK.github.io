---
layout: post
title: K-Tech 현장실습 - Oracle DBMS & Toad로 DB 실습
categories:
  - Other
---

## 프로젝트 개요
 - 교육용으로 집필 중인 Database 기본 개념서의 내용이 학생 수준에서 적당한지 검토
 - SQL 예제에 알맞는 테이블 및 데이터를 생성하여 예제 검증 및 예제 결과 기록
 - 현재 내 파트 : 테이블 생성 및 알맞은 데이터 삽입
 - DBMS : Oracle Database XE Release 18.4.0.0.0 (18c), TOAD(Freeware)
 - 작업인원 : 실습생 2명

## 준비과정

### 1. DBMS 설치
[오라클 DBMS 다운로드](https://www.oracle.com/database/technologies/xe-downloads.html)  
[TOAD 다운로드](https://www.toadworld.com/)

### 2. 초기 설정

#### 오라클 DBMS 설치 후 작동 확인 방법
> - **Windows + R** key를 누르고 `services.msc`를 입력
> - 서비스 창이 나오면 `OracleServvicesXE`를 찾아 **오른쪽 마우스-속성**을 누르고, **시작 유형 : 자동** 으로 설정
> - 서비스가 시작되어 실행 중임을 확인 후 닫기
> - **Windows + R** key를 누르고 `cmd` 를 입력
> - 커맨드 창이 나오면 `tnsping 127.0.0.1` 입력
> - 정상적으로 실행되고 마지막에 "확인(n밀리초)" 라고 나오면 성공

#### TOAD 설치 후 초기 화면 진입
![DB_Book_Toad](/assets/images/Other/DB_book_toad.PNG)  
![DB_Book_Toad](/assets/images/Other/DB_book_toad_login.PNG)  
로그인 후 접속하면, 아래와 같은 화면이 나옵니다.  
![DB_Book_Toad](/assets/images/Other/DB_book_toad_main_1.PNG)  
다음과 같이 명령어를 입력 후(1) 초록색 시작 버튼(2)을 누르게 되면 하단에 결과가 나오게 됩니다.  
만약 단축키를 이용하여 여러 줄의 질의를 동시에 수행하려면, F5키를 누르고 아래 사진처럼 조회합니다.
![DB_Book_Toad](/assets/images/Other/DB_book_toad_main_2.PNG)  


## 테이블 생성
```sql
create table department
    (dname varchar(10), 
     dean varchar(10),
     primary key (dname));

create table student
	(sno    int,
	 sname	varchar(20)	not null,
	 year	int,
	 dname  varchar(10),
	 primary key (sno),
     foreign key (dname) references department);

create table professor
	(pno    int,
	 pname	varchar(20)	not null,
	 salary numeric (6,2),
     dname  varchar(10),  
	 primary key (pno),
	 foreign key (dname) references department);

create table course
	(cno	number,
	 cname  varchar2(20),
	 dname  varchar(10),
     primary key (cno),
     foreign key (dname) references department);

create table take_course 
    (sno int,
     cno int,
     pno int,
     primary key (sno, cno, pno);
     
create table teach_course
    (pno int,
     cno int,
	 dname varchar(10),
     term int,
     year int,
     primary key (pno, cno, term, year),
     foreign key (dname) references department);
```

## 데이터 추가

```sql
insert into (table name) values (value, value, ... , value);
```

![DB_Book_Table_department](/assets/images/Other/DB_book_talbe/1_department_Table.PNG)
![DB_Book_Table_student](/assets/images/Other/DB_book_talbe/2_student_Table.PNG)
![DB_Book_Table_professor](/assets/images/Other/DB_book_talbe/3_professor_Table.PNG)
![DB_Book_Table_course](/assets/images/Other/DB_book_talbe/4_course_Table.PNG)
![DB_Book_Table_take_course](/assets/images/Other/DB_book_talbe/5_take_course_Table.PNG)
![DB_Book_Table_teach_course_1](/assets/images/Other/DB_book_talbe/6_1_teach_course_Table.PNG)
![DB_Book_Table_teach_course_2](/assets/images/Other/DB_book_talbe/6_2_teach_course_Table.PNG)


## 구현에서 어려웠던 점

- Web Version의 MySQL만 사용해 보다가 직접 로컬 DB를 구축해 보려 하니 쉽지 않았다. 학과 공부와 자격증 공부로 학습했던 이론과 다른 부분들도 많았다. 진행하면서 발생한 오류들은 Google 검색을 통해 해결하였고, 
- 예제를 보고 DB의 데이터를 만들어야 했는데, 쉽지 않았다. 질의에 적합한 답이 나오도록 데이터를 구상해야 했고, 오류가 있는 부분은 의도를 파악해서 수정했다.
- DB를 Export해서 다음 작업자에게 넘기는 과정에서 알 수 없는 오류로 Import가 되지 않았다. 차선책으로 Excel 파일로 Export하여 수동으로 Import시키는 방법으로 해결했다.