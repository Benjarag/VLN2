from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

from mail.models import Email


def mail_view(request):
    if request.method == 'POST':
        subject = request.POST.get('subject', 'Email from Castle Apartments')
        message = request.POST.get('message', 'This is a test email from Castle Apartments.')
        recipient = request.POST.get('recipient', '')

        if not recipient:
            messages.error(request, "Recipient email is required")
            return render(request, 'mail/email_form.html')

        _, success = send_system_email(
            recipient_email=recipient,
            sender_email=settings.EMAIL_HOST_USER,
            subject=subject,
            message=message
        )

        if success:
            messages.success(request, "Email sent successfully!")
            return redirect('home:homepage')  # Or wherever you want to redirect
        else:
            messages.error(request, "Failed to send email. Please try again later.")

    return render(request, 'mail/email_form.html')


def send_offer_notification_to_seller(offer):
    """Send an email notification to the property seller when a new offer is submitted"""
    buyer_name = offer.user.username
    seller_name = offer.seller.user.username if hasattr(offer.seller, 'user') else "Seller"
    seller_email = offer.seller.email
    
    if not seller_email:
        return False
        
    # Get expiration date from the appropriate field
    expiration_date = getattr(offer, 'date_expired', None)
    if not expiration_date and hasattr(offer, 'expiration_date'):
        expiration_date = offer.expiration_date
        
    expiration_text = expiration_date.strftime('%d-%m-%Y') if expiration_date else "N/A"
    
    subject = f"Property update on {offer.property_name}"
    message = f"""Hello dear {seller_name},

    {buyer_name} has submitted a purchase offer for your property "{offer.property_name}".
    
    Offer Details:
    - Offer Price: {offer.get_formatted_price()}
    - Expiration Date: {expiration_text}
    
    You can review and respond to this offer by logging into your Castle Apartments account.
    
    Best regards,
    Castle Apartments Team"""
    
    _, success = send_system_email(
        recipient_email=seller_email,
        sender_email=settings.EMAIL_HOST_USER,
        subject=subject,
        message=message
    )
    
    return success


def send_offer_status_notification_to_buyer(offer):
    """Send an email notification to the buyer when a seller updates the status of their offer"""
    buyer_email = offer.user.email
    if not buyer_email:
        return False

    status = offer.status
    subject = f"Your Offer for {offer.property_name} has been {status}"

    # Message templates with consistent indentation
    if status == 'Accepted':
        message = f"""Dear {offer.user.first_name or offer.user.username},

    Great news! Your offer of {offer.get_formatted_price()} for the property "{offer.property_name}" has been ACCEPTED.

    Next steps:
    - Our team will contact you shortly to discuss the closing process
    - Be prepared to complete the necessary paperwork
    - Start planning your move!

    Thank you for choosing Castle Apartments.

    Best regards,
    Castle Apartments Team"""
    elif status == 'Rejected':
        message = f"""Dear {offer.user.first_name or offer.user.username},

    We're sorry to inform you that your offer of {offer.get_formatted_price()} for the property "{offer.property_name}" has been REJECTED.

    Don't be discouraged! We have many other great properties available. 
    Keep browsing our listings to find your perfect home.

    Best regards,
    Castle Apartments Team"""
    else:
        message = f"""Dear {offer.user.first_name or offer.user.username},

    The status of your offer of {offer.get_formatted_price()} for the property "{offer.property_name}" has been updated to {status}.

    Please log into your Castle Apartments account for more details.

    Best regards,
    Castle Apartments Team"""

    seller_email = offer.seller.email if offer.seller and offer.seller.email else settings.EMAIL_HOST_USER

    _, success = send_system_email(
        recipient_email=buyer_email,
        sender_email=seller_email,
        subject=subject,
        message=message
    )

    return success


def send_system_email(recipient_email, sender_email, subject, message):
    """
    Centralized function to send emails and record them in the database.
    Returns (email_record, success)
    """
    from_email = settings.EMAIL_HOST_USER
    
    # Create database record
    email_record = Email.objects.create(
        buyer=recipient_email,
        seller=sender_email,
        subject=subject,
        message=message
    )
    
    try:
        # Send the email
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=[recipient_email],
            fail_silently=False,
        )
        return email_record, True
    except Exception as e:
        # Update status to failed
        email_record.status = 'failed'
        email_record.save()
        return email_record, False