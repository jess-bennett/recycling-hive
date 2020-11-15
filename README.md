# Recycling Hive :recycle:

<p align="center"> :recycle: <strong>Welcome to Recycling Hive!</strong> :recycle: <br>
Thanks for coming to take a look.
Recycling Hive is a place for community members to find out what they can recycle locally, and where. This allows the environmentally-conscious of us to recycle above and beyond what our local authority accepts.</p>

## Contents

[:sparkles: UX](#sparkles-ux)\
\
              [:books: User Stories](#books-user-stories)\
\
              [:earth_africa: Scope Plane](#earth_africa-scope-plane)\
\
              [:rainbow: Surface Plane/Design Choices](#rainbow-surface-planedesign-choices)\
\
              [:clipboard: Wireframes](#clipboard-wireframes)\
\
              [:dvd: Database Design](#dvd-database-design)\
\
              [:crystal_ball: Future Developments](#crystal_ball-future-developments)\
\
[:construction: Development Process](#construction-development-process)\
\
              [:unlock: Technologies Used](#unlock-technologies-used)\
\
              [:computer: External Sources Used](#computer-external-sources-used)\
\
              [:bug: Bugs](#bug-bugs)\
\
              [:broom: Refactoring](#broom-refactoring)\
\
              [:deciduous_tree: Branches](#deciduous_tree-branches)\
\
[:test_tube: Testing](#test_tube-testing)\
\
              [:raising_hand: Target-User Tests](#raising_hand-target-user-tests)\
\
              [:people_holding_hands: Peer Tests](#people_holding_hands-peer-tests)\
\
              [:memo: Manual Tests](#memo-manual-tests)\
\
              [:heavy_check_mark: W3C Tests](#heavy_check_mark-w3c-tests)\
\
              [:rotating_light: Lighthouse Tests](#rotating_light-lighthouse-tests)\
\
[:flight_departure: Deployment](#flight_departure-deployment)\
\
[:clapper: Credits](#clapper-credits)\
\
              [:movie_camera: Media](#movie_camera-media)\
\
              [:trophy: Acknowledgements](#trophy-acknowledgements)

## :sparkles: UX

The idea for this project comes from a zero-waste/recycling community on Facebook that I am an active member of. 

A large part of the group is built around dedicated individuals who collect a multitude of items that cannot be recycled via our local authority 
and arrange for these items to be sent to companies that do have the ability to recycle them. These individuals do this completely voluntarily and 
save incredible amounts of waste from going to landfill. Whilst I have co-ordinated collections myself in the past, I tend to be more of a waste-contributor
than a waste-collector. So, I wanted to give something back to this amazing group by creating this site.

Currently, all the recycling locations for the group are stored in an Excel spreadsheet which has become very unwieldy as it grows and is hard to keep up-to-date. My hope
in creating this site is that not only will this save the admin team a great deal of time, but will also make it easier for local community members to find out
what they can recycle, and where.

My eventual aim for the site is to offer it to other similar groups across the UK so that more people can find a Hive close to them where they can save more 
rubbish from landfill.

<em>Disclaimer: I think it is also important to point out here that recycling is <strong>not</strong> the answer, it is the last resort: 
'rethink, repair, refuse, repurpose, reduce, re-use, recycle'. However, if something <strong>can</strong> be recycled, it <strong>should</strong> be recycled.</em>

### :books: User Stories
---
* :woman: **Site Owner**
    * <strong>As a user</strong> I want a site that can be easily replicated for different Hives across the UK
    * <strong>As a user</strong> I want minimal ongoing maintenance work - the majority should be undertaken by the Queen Bees (admin) of each Hive

* :honeybee: **Queen Bee**
    * <strong>As a user</strong> I want to be able to maintain the membership database, with full CRUD accessibility
    * <strong>As a user</strong> I want to be notified when one of my Worker Bees adds or updates a recycling locations
    * <strong>As a user</strong> I want to have full CRUD accessibility over all recycling locations within my Hive

* :honeybee: **Worker Bee**
    * <strong>As a user</strong> I want to have full CRUD accessibility over the recycling locations that I add to the Hive

* :honeybee: **Busy Bee**
    * <strong>As a user</strong> I want to be able to easily find what items I can recycle locally, and where
    * <strong>As a user</strong> I want to be able to make suggestions about items that can be recycled nationally


### :earth_africa: Scope Plane
---
* :loop: **Site Logic**\
**Membership types**

| Membership | Approval                                                   | Notes                                                                                                                                           |
|------------|------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------|
| SuperUser  | N/A                                                        | The SU is the site owner - and the person responsible for the Mongo DB                                                                          |
| Queen Bees | First person to request a Hive location is given QB access | A current QB can request additional QBs (up to a max of 4 per Hive) to the SU                                                                   |
|            |                                                            | QBs cannot be deleted. A request must be made to the SU to first demote them and the profile can then be kept (as WB or BB) or deleted entirely |
|            |                                                            | If a Hive has only one QB, they must find and approve another QB before they can be removed                                                     |
| Worker Bee | Approved by QBs upon adding a new recycling location       | Once WB status has been given, all future private locations are automatically approved                                                          |                                             |
| Busy Bees  | Approved by QBs on completion of registration              | Each Hive will set their own security questions for registration so they can monitor new member requests                                        |

**Site access**
| Collection             | QB Access         | WB Access                  | BB Access            |
|------------------------|-------------------|----------------------------|----------------------|
| hives                  | :x:               | :x:                        | :x:                  |
| hiveMembers            | RUD for own Hive  | CRUD for own profile       | CRUD for own profile |
| collectionLocations    | RUD for own Hive  | CRUD for own location(s)   | R                    |
| itemCollections        | CRUD for own Hive | CRUD for own collection(s) | R                    |
| publicCollections      | CRU               | CR                         | CR                   |
| firstCollection        | RUD for own Hive  | :x:                        | C                    |
| itemCategory           | CR                | CR                         | CR                   |
| recyclableItems        | CR                | CR                         | CR                   |

<em><strong>CRUD = C</strong>reate, <strong>R</strong>ead, <strong>U</strong>pdate, <strong>D</strong>elete</em>

### :rainbow: Surface Plane/Design Choices
---
:pencil2: **Font families**

I decided to go for a 'handwritten' style of font for the entirety of the site. I chose this as I felt it would contribute to the 'community noticeboard' feel I was aiming for.

[Neucha](https://fonts.google.com/specimen/Neucha)
![Neucha Font](/wireframes/font-family.jpg)

:art: **Colour choices**

I chose fairly typical colours for a site revolving around recycling and the environment, based on a recycling image that I particularly liked from [here](https://blog.ferrovial.com/en/2016/11/recycling-began-when-greeks-discovered-landfills/)

The highlighted row is the main colour used throughout, with buttons and flash messages using varying shades of the same colour. Font colour was an off-black (#333) and in the vast majority of cases, was placed over an off-white (#fafafa) background for improved readibility.

![Site Colours](/wireframes/site-colours.jpg)

### :clipboard: Wireframes
---
The site was designed with a mobile-first approach. 

[Wireframe document can be seen here](/wireframes/wireframe.pdf)


:bulb: **Deviation from wireframe**

There was quite a lot of deviation from the original wireframe plan. This was mostly due to underestimating the complexity of the final database and also making better design decisions as my understanding/proficiency improved.\
The majority of the deviation was in the form of creating entirely new pages for the site. Whereas pages that were originally planned for have mostly stayed true to the original concept. 

I had also originally designed a lot of the content to be displayed in modals. As I began to delve more into Flask, I realised that additional pages (rather than modals) would be a much more preferable option!

#### Homepage
* The hexagon design on the homepage has been altered to be in-keeping with the rest of the site.
* I decided to include a link to the FAQs on this page to make them more accessible.
* Rather than requesting the site-visitor register in order to view the demo-site, I opted to make it instantly accessible to reach more potential members.

#### FAQs
* Very few deviations, except I had originally planned to have an image on this page. I eventually decided against it as I felt that an image would be at odds with the look of the rest of the site.

#### Register - Find a Hive
* This was in part a design choice, and in part due to prioritising other parts of the site. I had originally planned to have a searchable map using the Google Maps API.\
However, I decided to stick with the hexagon layout to show the currently available Hives. This might be something I go back to in the future.

#### Register
* Have included a link to the login page for those that have already registered. 
* Have included a link to the contact page for those that could not find a local hive.

#### Homepage - for logged-in users
* This page ended up with additional links to pages that hadn't been planned for:
    * Add collection
    * Contact
    * Manage Hive (for Queen Bees)
* I also included a link to the FAQs to make them more accessible. 
* The 'Be inspired' page and its link were removed altogether (as explained further down).
* I also decided to add a notification bar. This was following feedback from my first round of tests, as testers felt that communication within the site was lacking.

#### Profile
* This remained largely the same, except for the addition of another card to show public collections that had been added by the user

#### Hive
This has probably had the biggest overhaul from how it was originally envisaged.\
In reality, it is the most important part of the site - its sole purpose really! And it was difficult to find a design that was visually-appealing, clear and comprehensible, and
that also worked well with the database design. I hope I have managed to meet all those goals in the end.
* The original 'Explore categories' page was used as the main design for all new pages. 
* Rather than using cards and dropdowns as I had originally planned, I decided to split all the content into several new pages. This achieved:
    * More visual appeal than using a table-design as shown in the wireframe
    * A much clearer layout with fewer buttons and filters grouped onto a single page
    * A better way to work with Flask as it allowed me to separate my functions into different routes for different pages

#### Add New Location - modal
This concept also went through several iterations before I was happy with how it worked. The original idea was to have two separate modals - one for adding private/personal collections
and one for adding public collections. However, I was concerned that what seemed obvious to me (i.e. what type of collection it would be) might not be obvious to the user. 

In the end, I have chosen to have a single page for adding all new collections. This page is then routed through radio buttons that hide/display relevant content via JS.\
This means that the site does the work of deciding what goes where, rather than the user.

#### Be Inspired
This page was completely abandoned. Originally, it was going to be a place to display a randomly picked national collection, to inspire people to recycle something they hadn't thought of/
searched for. I was also going to give links to other sites that would be useful to people wanting to do more for the environment. However, I quickly realised that I had more than enough to be
getting on with and so left this page for a future development.

#### Contact page
This page was added despite not being on the original wireframe as I wanted a way for site-users to be able to get in touch with me easily. And in particular, if new visitors wanted to set up a Hive, they
needed a way to tell me!

#### Hive Management
My initial plan was for the Queen Bee(s) to do all of their admin within the original site pages. So for each collection displayed on the main Hive pages, they would have access to edit/delete buttons
to make any necessary amends. However, I soon realised that as the collections grow, it will get harder and harder to maintain without a central page for administration. 
Once I had decided to add this page, I used it as a place for all Queen Bee activity - accepting/deleting members, promoting to Worker Bee, accepting public collections...


### :dvd: Database Design
---
I opted for a document-oriented NoSQL database (MongoDB) and spent a large part of my planning time designing the database.

I initially ended up with the following six collections:

![Initial Database Model](/wireframes/database-model-initial.png)

However, as the site grew more complex, so did my database design. I ended up with eight collections:

![Final Database Model](/wireframes/database-model-final.png)

The key changes were:

#### hives
 * Added securityQuestion field so that each new Hive could set their own question for registration

#### hiveMembers
 * Added fields to store registration responses to security and marketing questions
 * Added approvedMember field to block parts of the site from the member until their registration has been approved

#### itemCategory/typeOfWaste
 * Added _lower fields to both to allow for easier matching on newly added documents - to avoid duplication

#### collectionLocations
 * Removed hiveID field as this is covered by the memberID
 * Added nickname and nickname_lower fields to allow a member to store more than one location (e.g. Home/Work) and easily distinguish between the two

#### itemCollections
 * Removed isNational field as this is now covered by the new 'publicCollections' collection

#### firstCollection
 * This is a new, temporary collection for storage of the first collection a member adds.\
 Its purpose is to allow the Queen Bee(s) to check all information given, before comitting it to the permanent 'itemCollections' collection.\
 By putting it in its own collection (rather than having a boolean field in 'itemCollections' to indicate a first collection), there was less searching required to find relevant
 documents for Queen Bee approval on the Hive Management page.

#### publicCollections
 * This is another new collection to store details of public collections. I felt putting these details in a separate collection (rather than using the 'isNational' boolean field
 I had originally planned on), was a more straightforward approach as some of the data fields needed for this collection were slightly different.


In hindsight, I realise that using a NoSQL database for this website might not have been the ideal approach. However, it has given me a huge amount of experience using MongoDB, so all
is not lost.

### :crystal_ball: Future Developments
---

As this site is intended to be used by my local community, and potentially other communities in the future, there is a lot more that I would like to do with it.\
At this stage, I have had to make some difficult decisions about when to stop working on it so that I can actually submit it.\
It will definitely be an ongoing project and some ideas I am already thinking about are:

* Changing the 'Find a Hive' page to include a searchable map - if there are enough Hives set up to warrant this.
* Creating the 'Be Inspired' page to showcase alternatives to single-use products, and promote sites with a similar ethos
* Adding a forum/messaging system so that members of a Hive can communicate with each other
* Including additional information in the hive collection modals - for example, a telephone number/email address field for relevant cases
* Adding a search facility to find recyclable items more quickly

## :construction: Development Process

### :unlock: Technologies Used
---
**Languages**
* [CSS](https://developer.mozilla.org/en-US/docs/Web/CSS)
* [HTML](https://developer.mozilla.org/en-US/docs/Web/HTML)
* [Javascript](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
* [Python](https://www.python.org/)

**Libraries & Frameworks**
* [Bootstrap](https://getbootstrap.com/)
* [Font Awesome](https://fontawesome.com/)
* [Google Fonts](https://fonts.google.com/)
* [jQuery](https://jquery.com/)
* [Popper](https://popper.js.org/)
* [Flask](https://flask.palletsprojects.com/en/1.1.x/)

**Tools**
* [GitHub](https://github.com/)
* [Gitpod](https://gitpod.io/)
* [Heroku](https://heroku.com/)
* [MongoDB](https://www.mongodb.com/)
* [Favicon.io](https://favicon.io/)


### :computer: External Sources Used
---

* Honeycomb background
    * The effect for the header/footer was adapted from code taken from [here](https://projects.verou.me/css3patterns/#honeycomb)

* Hexagon grid layout
    * This layout was adapted (with some difficulty!) from the code and tutorial on [Codesmite.com](https://www.codesmite.com/article/how-to-create-pure-css-hexagonal-grids)

* Email
    * The JS required to send emails through the contact form was from [EmailJS.com](https://www.emailjs.com/)

* Password validation
    * The password validation JS was adapted from an explanation given on [Stackoverflow.com](https://stackoverflow.com/questions/21727317/how-to-check-confirm-password-field-in-form-without-reloading-page/21727518)

* Favicon
    * Generated using [Favicon.io](https://favicon.io/)

### :bug: Bugs
---
#### Bug 1
A main cause of issues during the creation of this project concerned the hexagon grid layout.\
I didn't want to abandon the css entirely as I am overall very pleased with how it looks and how 
it ties in with the overall theme of the sight, and so I had to find some workarounds in order for
it to behave as I needed.
The spacing on the hive-category page was one such issue, with the hexagon grid overlapping the 
breadcrumb navbar at the top. 
My workaround was to include a button as on the other pages (where spacing was not an issue), but
set the button's visibility to hidden.
<hr>

#### Bug 2
Less of a bug, and more of a complex solution to an issue...
I was suprised to find that there was no easy solution to displaying text if a jinja 'for loop' was empty.\
Essentially, on the hive members page, I wanted to display a list of all of the collections relevant to the selected member. 
The 'for loop' worked perfectly to display their data, but for members without a collection, the list was blank. In this scenario I wanted
to display some text to signify to the user that this was not an error, but instead that there were no collections to display. 

<strong>Initial working code</strong>
```html
{% for collection in membersDict if collection._id == member._id %}
    {% include "components/collection-details-modal.html" %}
{% endfor %}
```
This first piece of code displayed data, but no text for collection-less members. 

<strong>First adjustment</strong>
```html
{% for collection in membersDict %}
    {% if collection._id == member._id %}
        {% include "components/collection-details-modal.html" %}
    {% else %}
    <p>No collection to display</p>
    {% endif %}
{% endfor %}
```
After the first adjustment, the data was displayed correctly for members with a collection.
For members without a collection, the text was repeated by the total number of collections.

I tried many other solutions including variations of:\
<strong>Second adjustment</strong>
```html
{% if member._id in membersDict %}
    {% for collection in membersDict if collection._id == member._id %}
        {% include "components/collection-details-modal.html" %}
    {% endfor %}
    {% else %}
    <p>No collection to display</p>
{% endif %}
```
But none of these worked as 'membersDict' is a nested list and so 'member._id' could not be found.

What appeared to be the perfect solution in Python:\
<strong>Third adjustment</strong>
```html
{% if (any(member._id in x for x in membersDict)) %}
    {% for collection in membersDict if collection._id == member._id %}
        {% include "components/collection-details-modal.html" %}
    {% endfor %}
    {% else %}
    <p>No collection to display</p>
{% endif %}
```
Did not translate to Jinja and so this adjustment did nothing.

<strong>Solution</strong>
```html
{% if member._id in membersCollectionValues %}
    {% for collection in membersDict if collection._id == member._id %}
        {% include "components/collection-details-modal.html" %}
    {% endfor %}
    {% else %}
    <p>No collection to display</p>
{% endif %}
```
The only solution that I was able to find that worked, was to create a new <strong>un-nested</strong> list in my
Flask route, which contained all the member IDs with collections. I was then able to search this list
to enable my 'if statement'.

I am still not convinced that this is the most elegant solution, but it was the best I was able to come up with for this issue!

### :broom: Refactoring
---
As my app.py file grew quite large and unwieldy, I needed to do some refactoring to ensure everything was in the right place, and to try and keep my code as DRY as possible.

To do this, I created a utilities.py file and moved any helper functions there.

For now, I have just done this for anywhere that there were large duplications of code. This has resulted in a reduction in the app.py file of 530 lines of code.

In future, I would make more use of a utilities file and ensure that only logic-based/routing code is kept in the app.py file.

A further improvement would be to reduce some of the repeated code in my various components. For example, tooltips and modals. However, I have decided against refactoring this as I 
am reluctant to undo too much of the work I have already done. This is something I will take forward into my next project.


### :deciduous_tree: Branches
---

The majority of the build was carried out in a Development branch with additional sub-branches being pulled through as work was completed. 

Prior to testing, all working code was pulled through into the Master branch and amends from testing feedback have all been pulled directly into the Master branch from sub-branches.

## :test_tube: Testing  

Throughout the build, all functions were continually tested as new functionality was added. This was carried out with the help of Google Dev Tools to ensure that new features worked and displayed as expected on mobile, tablet and desktop views.

Once the majority of the site was built, I turned to user testing. The user tests were designed to not only test aesthetics and functionality, but also the database and whether data was committed correctly.

### :people_holding_hands: Peer Tests
---
The first stage of external testing was carried out by my family.

They were given an explanation on how their data would be used within the site:

<img src="testing/testing_instructions.jpg" alt="Data explanation" width="400">

They each also had specific instructions relating to a user-story to ensure that all functions were fully tested.

[Queen Bee instructions](/testing/testing_instructions_jane.pdf)\
[Worker Bee instructions](/testing/testing_instructions_tom.pdf)\
[Busy Bee instructions](/testing/testing_instructions_chris.pdf)

Feedback from this was good with no suggestions for change from Jane or Chris.

Tom had some suggestions which are shown on the [Testing Feedback document](/testing/testing_feedback.pdf).

Having acted on the feedback from the Peer Tests I moved onto Target User Tests.

### :raising_hand: Target User Tests
---

These tests were conducted by volunteers from the Facebook group that inspired this project. In total, there were 6 testers.

They were given the same data explanation as the peer testers:
[Data explanation](/testing/testing_instructions.pdf)

Both Jenny and Hannah encountered an error message which was not picked up by the Python error handler. Fortuntately, they screenshotted the error so I was able to 
confirm that it was caused by some work I was doing whilst they were testing. The error has not happened since.

Otherwise, feedback was very positive, with some suggestions for cosmetic/functional improvements:
![Testing Feedback document](/testing/testing_feedback.jpg)

The majority of the feedback was acted upon (highlighted in green on the document) and improvements were made to the site. All of the suggestions were very good, but time constraints have meant that I cannot implement all of them.
Those that are not being put in place now, have been put in the [Future Developments](#crystal_ball-future-developments) section of this README.

### :memo: Manual Tests
---
Manual testing was carried out on all devices available to me:
* Google Dev Tools:
    * Mobile device
    * iPad vertical
    * iPad horizontal
    * Desktop

* Published site:
    * Samsung Galaxy S8
    * Desktop

* Browser
    * Chrome
    * Edge
    * Firefox
    * Safari (Using [Lambdatest](https://www.lambdatest.com/))
    * Opera 

All tests produced good results with the following exceptions:
TBC

Full testing-frame can be found [here](/testing/testing-frame.pdf)
TBC

### :heavy_check_mark: Online Validators
---

TBC

### :rotating_light: Lighthouse Tests
---

[Lighthouse Test results](/testing/lighthouse_tests.pdf)

The results of the Lighthouse Tests were generally good. Some minor amends were made to the code following the first round of tests:
* Moved tooltip text from div to anchor in footers for sr accessibility
* Added noreferrer to external links for improved security
* Added meta description

Accessibility required improvement on some pages:
* There were still some issues with the title text used in the footer links, despite it being there. No further amends were possible. 
* Duplicate IDs were picked up in aria-labels, but I was unable to identify any duplicates and therefore could not make any improvements.


## :flight_departure: Deployment 

Recycling Hive :recycle: was developed in [Gitpod](https://gitpod.io/), hosted on [GitHub](https://github.com/) and deployed to [Heroku](https://heroku.com/)

### Cloning Recycling Hive :recycle: from GitHub

You will need to recreate the database in [MongoDB](https://www.mongodb.com/)

<strong>The following instructions are for a Windows OS only. Please consult your OS for python commands.</strong>

1. Clone the Recycling Hive :recycle: repository by downloading it from [here](https://github.com/jess-bennett/recycling-hive),
or if you have Git installed you can type the following into the CLI:
```
git clone https://github.com/jess-bennett/recycling-hive
```

2. Within the new folder, type the following into the CLI:
```
python3 -m .venv venv
```

3. And initialise the environment with:
```
.venv\Scripts\activate 
```

4. Install the necessary requirements from the requirements.txt file:
```
pip3 -r requirements.txt
```

5. Create a file named 'env.py' with the structure below and replace the SECRET_KEY, MONGO_URI, MONGO_DBNAME and DEMO_ID* with your own values
```
import os

os.environ.setdefault("IP", "0.0.0.0")
os.environ.setdefault("PORT", "5000")
os.environ.setdefault("SECRET_KEY", "<your_secret_key>")
os.environ.setdefault("MONGO_URI", "<your_mongo_uri>")
os.environ.setdefault("MONGO_DBNAME", "<your_mongo_dbname>")
os.environ.setdefault("DEMO_ID", "<your_demo_id>")
```
<em>*The Demo_ID should be the _id of a hiveMember using fictitious details</em>

6. The application can now be run using:
```
python3 app.py
```

### Deploying Recycling Hive :recycle: to Heroku

1. Create a requirements.txt file by typing the following into your CLI:
```
pip3 freeze > requirements.txt
```

2. Push to your repository, create a new app on the Heroku Dashboard

3. Change the deployment method to Github and ensure the app is connected and automatic deploys are enabled (if you wish)

4. In Settings, set the Config Vars as follows:

| Key          | Value                                                      |
|--------------|------------------------------------------------------------|
| IP           | 0.0.0.0                                                    |
| MONGO_DBNAME | <your_mongo_dbname>                                        |
| MONGO_URI    | mongodb+srv://<your_username>:<your_password>@<your_cluster_name>.<br>6abok.mongodb.net/<your_database_name>?retryWrites=true&w=majority |
| PORT         | 5000                                                       |
| SECRET_KEY   | <your_secret_key>                                          |
| DEMO_ID      | <your_demo_id>                                          |

5. Deploy the app from the Heroku dashboard and open the app

## :clapper: Credits

### :movie_camera: Media
---

Images for Home Page navigation grid were taken from [Font Awesome's SVGs](https://github.com/FortAwesome/Font-Awesome/tree/master/svgs/regular)

### :trophy: Acknowledgements
---
I would like to thank the following people for their help and support with this project:

:recycle: Firstly, it has to be the entire 'Thatcham & Newbury plastic free, recycling & zero waste uk' Facebook group
The work of the group members was the sole inspiration behind this project and the knowledge that is shared there is an inspiration!

:recycle: Following this, I would like to thank the group moderators for their advice and support before starting this project:
Jana Karstova Little, Jacky Akam, Jenny Kirby and Paula Smalley

:recycle: With another special mention to the group members who kindly volunteered to help with testing - and went far above and beyond what I expected in terms of feedback:
Hannah Marsh, Jenny Kirby, Jo Hands, Linda Mary, Merlin (Georgia!) Jackson and Nikki Coome

:star: My husband, Tom - for being a very patient and encouraging site-tester and brain-storming partner. Also for endless hours at the park with Eddie so I could work!

:star: My parents, Jane & Chris - for their patience and encouragement as site-testers.

:star: Never forgetting my incredibly dedicated mentor, [Simen](https://www.linkedin.com/in/simendaehlin/). The tips and advice on improving my code are always appreciated!