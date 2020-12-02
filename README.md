# Micro-Volunteering and Micro-Donations Web Application
### Developed by Commits4Charity (Team 1-37) 

## Log In
The web application authenticates with Google, so you need to have a Google account to use for login. 

## Welcome
### Displayed upon login and accessed by clicking Commits4Charity in the navbar
Upon login, you will be viewing the Welcome page. One of two messages are displayed:
- "Welcome, username!" - if you are not in the top 10
- "Congratulations, username! You have made it into the top ten!" - if you are in the top 10, additionally provides a button linking to the leaderboard so you can view your amazing accomplishment

Also displayed is a box with your current point value and quick links to the Volunteer and Donation listings. Signing up for volunteering events and donating to causes is how you earn points.

## Points System
**Points = Volunteering Hours x 10 + Donation Dollars**

The total number of points a user has is comprised of points for volunteering and donations. The number of volunteering hours they have signed up for is scaled by a factor of 10, because time is precious. The amount donated (in US dollars) directly corresponds to the number of points obtained.

## Leaderboard
### Accessed by clicking Leaderboard in the navbar

The top 10 users are displayed here in addition to a formula detailing the points system! 

## Volunteering Opportunities
### Accessed by clicking Volunteer in the navbar
Users can post and sign up for Volunteer Events here! Opportunities are listed in an accordion style, such that clicking the listing expands its details and allows a user to sign up. Opportunities also display the associated creator of the opportunity, and you can navigate to that person's profile by selecting their name fo contact them about the opportunity.

To sign up for an event, click the **Sign Up** button within the expandable detail window of an event. This signs you up for the event and redirects you to your personal page listing events that you have signed up for. The **Events I've Signed Up for** page is one of four pages that display events and donations specific to you - for more information on these pages, see the **My Volunteering and Donations** section.

To post a volunteer opportunity, click the **Post Volunteer Opportunity** button at the top of the **Volunteer** page. This opens a form for creating the event. The form fields are:
- Event Name
- Date and Time - the date and start time of the event
- Volunteering Hours - the length of the event in hours and minutes (HH:MM). This value is what will be used in points calculations
- Location
- Event Description
- Volunteers Needed - the number of volunteers needed at the event. When the sign up is full, the event will no longer be listed. 

Clicking the calendar or clock widgets are one way of providing *Date and Time* and *Volunteering Hours* respectively. Alternatively, these values can be typed.

## Donation Opportunities
### Accessed by clicking **Donate** in the navbar
Users can post and choose to donate to Donation Opportunities here! Donation Opportunities are listed in an accordian style, and clicking each listing shows details about the opportunity and allows a user to donate. Opportunities also display the associated creator of the opportunity, and you can navigate to that person's profile by selecting their name fo contact them about the opportunity.

To donate to a Donation Opportunity, click the **Donate** button within the expandable detail window. This will redirect you to a separate checkout page, where you can specify the amount you would like to donate. Once a valid amount is specified, selecting the blue "Pay with PayPal" will pop open a PayPal window/tab, where you can log into a PayPal account and  complete the transaction through PayPal. To see previous donations, the **Donation History** page will display previous donation details, including: the opportunity donated to, the amount donated, and the date the transaction was completed. 

To use our sandbox PayPal account, input these credentials into the PayPal popup:
- **Email:** customer137@gmail.com
- **Password:** project137

To post a Donation Opportunity, click the **Post Donation Opportunity** button at the top of the **Donate** page. This opens a form for creating the opportunity. The form fields are:
- Organization Name - if creating a donation opportunity on behalf of an organization, this is where that information would go
- Donation Opportunity Description
- Relevant Causes - you can select causes that are relevent to your organization/donation opportunity. These are displayed along with the donation opportunity to help users identify if the causes your opportunity stands for are relevant to them

## My Volunteering and Donations 

### Events - signed up for
Accessed by clicking the **Me** dropdown, then clicking **My Volunteering**

On this page, you can view the Volunteering Events you have signed up for. If you can no longer attend an event, you can select the event and click the **Remove** button to indicate this and remove the event from this page.

### Donation History
Accessed by clicking the **Me** dropdown, then clickign **My Donations**

On this page, you can view the previous donations you have made to different Donation Opportunities. You can see information such as the amount donated and the date the money was donated. You can not rescind a donation once it has been made.

### Created Events
Accessed by clicking the **Me** dropdown, then clicking **Created Volunteering**

On this page, you can view the Volunteering Events you have set up. As the creator of the Volunteer Events on this page, you have the option to delete any of these events as applicable.

### Created Donations
Accessed by clicking the **Me** dropdown, then clicking **Created Donations**

On this page, you can view the Donation Opportunities you have set up, and can also see information that is not visible to other users, such as the total amount the Donation has accrued. Unlike Volunteer Opportunities, Donation Opportunities, once created, can not be deleted.

## Profile
### Profile Page
Your personal profile page can be accessed by selecting the **Me** dropdown, then clicking **Profile**. On your profile, you can view basic information such as: Username, Name, Email, and the number of Points you have accrued.

### Profile Settings
If any of the information on you profile page is not to your liking, you can visit the profile settings page by selecting the **Me** dropdown and clicking **Settings**. On this page, you can change your username, first name, or last name, and save these settings by selecting the green **Save** button. If inputs are valid, this will redirect you to the **Profile** page, now with the new information. Any invalid inputs will cause the settings page to revert to its original form, but with an error message displayed at the top of the page.
