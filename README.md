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

Currently, all the recycling locations are stored in an Excel spreadsheet which has become very unwieldy as it grows and is hard to keep up to date. My hope
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

### :earth_africa: Scope Plane
---
* :loop: **Site Logic**\
**Membership types**
Membership | Approval | Notes
-----------|----------|-------
SuperUser | N/A | There is only one SU - ME!
Queen Bees | First person to request a Hive location is given QB access | A current QB can request additional QBs (up to a max of 4 per Hive) to the SU
| | QBs cannot be deleted. A request must be made to the SU to first demote them and the profile can then be kept (as WB or BB) or deleted entirely
| | If a Hive has only one QB, they must find and approve another QB before they can be removed
Worker Bee | Approved by QBs upon adding a new recycling location | Once WB status has been given, all future locations are automatically approved
| | Each newly added location will have a <strong>NEW</strong> flag for 7 days so that QBs can monitor
Busy Bees | Approved by QBs on completion of registration | Each Hive will set their own security questions for registration so they can monitor new member requests

**Site accessibility**
Collection | QB Access | WB Access | BB Access
-----------|-----------|-----------|-----------
Hive collection | :x: | :x: | :x:
Member collection | CRUD for own Hive | CRUD for own profile | CRUD for own profile
Location collection | CRUD for own Hive | CRUD for own location(s) | R
Item collection | CRUD for own Hive | CRUD for own collection(s) | R
Recyclables collection | CR | CR | R
Category collection | CR | CR | R

### :rainbow: Surface Plane/Design Choices
---
:pencil2: **Font families**

I decided to go for a 'handwritten' style of font for the entirety of the site. I chose this as I felt it would contribute to the 'community noticeboard' feel I was aiming for.

[Neucha](https://fonts.google.com/specimen/Neucha)
![Neucha Font](/wireframes/font-family.jpg)

:art: **Colour choices**

I chose fairly typical colours for a site revolving around recycling and the environment, based on a recycling image that I particularly liked from [here](https://blog.ferrovial.com/en/2016/11/recycling-began-when-greeks-discovered-landfills/)

![Site Colours](/wireframes/site-colours.jpg)

### :clipboard: Wireframes
---
The site was designed with a mobile-first approach. 

[Wireframe document can be seen here](/wireframes/data-centric-wireframe.pdf)


:bulb: **Deviation from wireframe**