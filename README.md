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
              [:broom: Clean-Up](#broom-clean-up)\
\
              [:deciduous_tree: Branches](#deciduous_tree-branches)\
\
[:test_tube: Testing](#test_tube-testing)\
\
              [:raising_hand: Target-User Tests](#raising_hand-target-user-tests)\
\
              [:people_holding_hands: Peer Tests](#people_holding_hands-peer-tests)\
\
              [:sparkle: Jasmine Tests](#sparkle-jasmine-tests)\
\
              [:memo: Manual Tests](#memo-manual-tests)\
\
              [:heavy_check_mark: W3C Tests](#heavy_check_mark-w3c-tests)\
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
    * As a user I want a site that can be easily replicated for different Hives across the UK
    * As a user I want minimal ongoing maintenance work - the majority should be undertaken by the Queen Bees (admin) of each Hive

* :honeybee: **Queen Bee**
    * As a user I want to be able to maintain the membership database, with full CRUD accessibility
    * As a user I want to be notified when one of my Worker Bees adds or updates a recycling locations
    * As a user I want to have full CRUD accessibility over all recycling locations within my Hive

* :honeybee: **Worker Bee**
    * As a user I want to have full CRUD accessibility over the recycling locations that I add to the Hive

* :honeybee: **Busy Bee**
    * As a user I want to be able to easily find what items I can recycle locally, and where
    * As a user I want to be able to make suggestions about items that can be recycled nationally

<em><strong>C</strong>reate, <strong>R</strong>ead, <strong>U</strong>pdate, <strong>D</strong>elete</em>

### :earth_africa: Scope Plane
---
* :loop: **Site Logic**\
**Membership types**

| Membership | Approval                                                   | Notes                                                                                                                                           |
|------------|------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------|
| SuperUser  | N/A                                                        | The SU is the site owner - and the person responsible for the Mongo DB                                                                                                                   |
| Queen Bees | First person to request a Hive location is given QB access | A current QB can request additional QBs (up to a max of 4 per Hive) to the SU                                                                   |
|            |                                                            | QBs cannot be deleted. A request must be made to the SU to first demote them and the profile can then be kept (as WB or BB) or deleted entirely |
|            |                                                            | If a Hive has only one QB, they must find and approve another QB before they can be removed                                                     |
| Worker Bee | Approved by QBs upon adding a new recycling location       | Once WB status has been given, all future private locations are automatically approved                                                          |                                             |
| Busy Bees  | Approved by QBs on completion of registration              | Each Hive will set their own security questions for registration so they can monitor new member requests                                        |

**Site accessibility**
| Collection             | QB Access         | WB Access                  | BB Access            |
|------------------------|-------------------|----------------------------|----------------------|
| Hive collection        | :x:               | :x:                        | :x:                  |
| Member collection      | CRUD for own Hive | CRUD for own profile       | CRUD for own profile |
| Location collection    | CRUD for own Hive | CRUD for own location(s)   | R                    |
| Item collection        | CRUD for own Hive | CRUD for own collection(s) | R                    |
| Recyclables collection | CR                | CR                         | R                    |
| Category collection    | CR                | CR                         | R                    |

### :rainbow: Surface Plane/Design Choices
---
:pencil2: **Font families**

I decided to go for a 'handwritten' style of font for the entirety of the site. I chose this as I felt it would contribute to the 'community noticeboard' feel I was aiming for.

[Neucha](https://fonts.google.com/specimen/Neucha)
![Neucha Font](/wireframes/font-family.jpg)

:art: **Colour choices**

I chose fairly typical colours for a site revolving around recycling and the environment, based on a recycling image that I particularly liked from [here](https://blog.ferrovial.com/en/2016/11/recycling-began-when-greeks-discovered-landfills/)

The highlighted row is the main colour used throughout, with buttons and flash messages using varying shades of the same colour. Font colour was an off-black and in the vast majority of cases, was placed over an off-whie background for improved readibility.

![Site Colours](/wireframes/site-colours.jpg)

### :clipboard: Wireframes
---
The site was designed with a mobile-first approach. 

[Wireframe document can be seen here](/wireframes/data-centric-wireframe.pdf)


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

#### Add new location modal
This concept also went through several iterations before I was happy with how it worked. The original idea was to have two separate modals - one for adding private/personal collections
and one for adding public collections. However, I was concerned that what seemed obvious to me (i.e. what type of collection it would be) might not be obvious to the user. 

In the end, I have chosen to have a single page for adding all new collections. This page is then routed through radio buttons that hide/display relevant content via JS.\
This means that the site does the work of deciding what goes where, rather than the user.

### :dvd: Database Design
---
I opted for a document-oriented NoSQL database (MongoDB) and spent a large part of my planning time designing the database.

I ended up with the following six collections:

![Database Model](/wireframes/database-model.jpg)

### :crystal_ball: Future Developments
---

## :construction: Development Process

### :unlock: Technologies Used
---
**Languages**
* [CSS](https://developer.mozilla.org/en-US/docs/Web/CSS)
* [HTML](https://developer.mozilla.org/en-US/docs/Web/HTML)
* [Javascript](https://developer.mozilla.org/en-US/docs/Web/JavaScript)

**Libraries & Frameworks**
* [Bootstrap](https://getbootstrap.com/)
* [Font Awesome](https://fontawesome.com/)
* [Google Fonts](https://fonts.google.com/)
* [jQuery](https://jquery.com/)
* [Popper](https://popper.js.org/)

**Tools**
* [Gimp (image editing)](https://www.gimp.org/)


### :computer: External Sources Used
---

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


### :deciduous_tree: Branches
---

## :test_tube: Testing  

### :raising_hand: Target User Tests
---

### :people_holding_hands: Peer Tests
---

### :sparkle: Jasmine Tests
---

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


Full testing-frame can be found [here](/testing/manual-testing.pdf)

### :heavy_check_mark: Online Validators
---

## :flight_departure: Deployment 

## :clapper: Credits

### :movie_camera: Media
---

### :trophy: Acknowledgements
---