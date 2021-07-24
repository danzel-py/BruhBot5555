# CS-B25 Discord Bot
last update : July 204th 2021

fix: multiple dailyQuotes() sent
## Features Available:

### 0. B$help

  - Info keyword + info bot

### 1. Reminder Deadline Tugas


Sends message to designated channel for each deadline on hour-1, minute-5, and on time.


#### help:
    
    B$help reminder

#### New Reminder:

    B$reminder (reminder_name) (date) (time) (tags)

examples:   

    B$reminder PRLinearAlgebraWeek1 02/02/2022 23:00 Kelas1
    B$reminder EnglishQuiz nextwed 4pm everyone
    B$reminder kick_all_member selasa 12.30 Admin
    B$reminder updateReadme today 8.50pm me 
    
+ tags: role (everyone, Admin, dll) , me.

#### Show Reminder Lists:

    B$listtoday
    B$listtomorrow
    B$listreminder

#### Undo Add Reminder:

Deletes last reminder entry
    
    B$undoreminder

### 2. Info Binus
  - Get new post from binus_bandung's instagram   

### 3. Other 

#### Weather
Show today's weather (brief)

    B$weathertoday
    
#### Table
Creates table with `-` separator

    B$table (*optional)
Optional arguments:
- `number`, shows indices
- `header`, makes first row as Header
- First col width in integer

example:

- Create a table with header, indices, and width 10 characters

        input:

        B$table 10 header number
        Ingredient-Quantity
        Flour-5 to 6 cups
        Salt-½ tsp
        Sugar-½ cups

        output:

        ╒════╤═════════════════╤═════════════╕
        │    │   Ingredient⠀   │ Quantity    │
        ╞════╪═════════════════╪═════════════╡
        │  0 │ Flour           │ 5 to 6 cups │
        ├────┼─────────────────┼─────────────┤
        │  1 │ Salt            │ ½ tsp       │
        ├────┼─────────────────┼─────────────┤
        │  2 │ Sugar           │ ½ cups      │
        ╘════╧═════════════════╧═════════════╛


####  Misc.

  Keyword nya `B$` gatau ntar ganti ato gimana

  ini masih ngasal sih, nanti di delete kayanya->

  - `B$inspire` : sends a random quote
  - `B$hello` : ya gitu

## TODO:

### 1. Reminder Deadline Tugas

  - ~~Need fancy command names~~
  - Minta admin bikin role kelas maybe

### 2. Info Binus
  - Create ig user lists to fetch posts from (currently only binus_bandung)

## Features - TOADD:


### 1. Reminder Jadwal Kuliah (blm yakin guna ato ga)

  - tfw blom dapet jadwal kuliah

  - ~~nanti bikin API get jadwal kuliah~~ : kalo niat

    - input jadwal kuliah  ke DB nya


