# VLN2::Extra Requirements 

## Seller
### The user shall be able to choose to sign-up as a seller.
#### Sellers can:
- A seller **can't** submit a purchase offer through their sellers' profile
- View their own listings 
- Access their listings on the 'My Listings' page which is available in the navigation bar
- View the offers made on their listings
- Access the offers made on their listings on the 'My Offers' page which is available in the navigation bar
- Accept, Reject or make offers Contingent on the 'My Offers' page
- Either be an agency seller or an individual seller

#### For each purchase offer, sellers can:
- See the **name of the property** associated with the offer
- Click a link to navigate to the **Property Details** page
- View the **date** the offer was submitted
- View the **expiration date** of the offer
- See the **current status** of the offer (Pending, Accepted, Rejected, or Contingent)
- See the **name of the buyer** who submitted the offer
- View the **offer price**
- If the offer status is **Pending**, select to **Accept**, **Reject**, or mark it as **Contingent**
- When an action is taken, the system **updates the status** of the offer accordingly

## Favorites
### The user shall be able to favorite any property
#### Users can:
- Click the 'heart' of a property listing and 'favorite' that property
- View all the favorited properties on the **Favorites** page
- Access the **Favorites** page via the navigation bar

#### Favorite page:
- Will save all properties that have been favorited by the user
- Displays the properties in a list similar to the property listings page
- Saves the favorites between sessions
- Allows users to 'un-heart' properties and removes them from the **Favorites** page
- The 'heart' will remain 'active' even when the user refreshes the page, and between sessions

## Profile Page 
### The user shall be able to update their profile
#### Buyers can:
- Update their username
- Add a profile picture
- Change their profile picture
- Add a phone number
- when a user adds a phone number, and/or a profile picture it is displayed in their profile page

#### Sellers can:
- Update their username
- Change their seller type (i.e. whether they are a agency or individual seller)
- Add or change their profile picture
- Add or change their logo
- Add or change their Street Address, city, and postal code
- Add or change their bio
- If they are an individual seller then only their phone-number will show up additionally on the profile page
- If they are an agency seller then the Street Address, city, and postal code, phone number, logo and bio will be displayed on the profile page

## Mail Service
### The system should be able to notify the buyers' and sellers' via email
#### The system can:
- notify the sellers when a property of theirs has received an offer.
- The sellers' email includes which property the offer has been made on, who made it, for what amount, and when.
- Notify the buyers' when a seller has made an action on their offer (i.e. accepted, rejected or made it contingent)
- The buyers' email includes which property status has been updated, for what price and congratulates them.

## System restriction
### If a guest attempts to perform a restricted action, the system shall redirect them to the login page and display the message: “Please log in or create an account to use this feature.”
#### The system does this when:
- A guest user tries to navigate to the **Favorites** page
- A guest user tries to navigate to the **Offers** page
- A guest user tries to 'heart' a listing

