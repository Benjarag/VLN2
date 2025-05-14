from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings

from mail.models import Email


def mail_view(request):
    if request.method == 'POST':
        subject = request.POST.get('subject', 'Email from Castle Apartments')
        message = request.POST.get('message', 'This is a test email from Castle Apartments.')
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [request.POST.get('recipient', '')]

        # Send email
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=from_email,
                recipient_list=recipient_list,
                fail_silently=False,
            )
            return HttpResponse("Email sent successfully!")
        except Exception as e:
            return HttpResponse(f"Failed to send email: {str(e)}")

    # If GET request, render an email form
    return render(request, 'mail/email_form.html')


def send_offer_notification_to_seller(offer):
    """
    Send an email notification to the property seller when a new offer is submitted
    """
    # Get buyer's name
    buyer_name = f"{offer.user.first_name} {offer.user.last_name}" if (
                offer.user.first_name and offer.user.last_name) else offer.user.username

    # Get seller's email - check if seller has email, otherwise use site admin email
    seller_email = offer.seller.email if offer.seller and offer.seller.email else settings.EMAIL_HOST_USER

    subject = f"Property update on {offer.property_name}"
    message = f"""
    Hello dear {offer.seller_name},

    {buyer_name} has submitted a purchase offer for your property "{offer.property_name}".

    Offer Details:
    - Offer Price: {offer.get_formatted_price()}
    - Expiration Date: {offer.date_expired.strftime('%d-%m-%Y')}

    You can review and respond to this offer by logging into your Castle Apartments account.

    Best regards,
    Castle Apartments Team
    """

    email_record = Email.objects.create(
        buyer=offer.user.email,
        seller=seller_email,
        subject=subject,
        message=message
    )

    # Send the email
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[seller_email],
        fail_silently=False,
    )

    return True


def send_offer_status_notification_to_buyer(offer):
    """
    Send an email notification to the buyer when a seller updates the status of their offer
    """
    # Get buyer's email
    buyer_email = offer.user.email

    status = offer.status
    subject = f"Your Offer for {offer.property_name} has been {status}"

    if status == 'Accepted':
        message = f"""
        Dear {offer.user.first_name or offer.user.username},

        Great news! Your offer of {offer.get_formatted_price()} for the property "{offer.property_name}" has been ACCEPTED.

        Next steps:
        - Our team will contact you shortly to discuss the closing process
        - Be prepared to complete the necessary paperwork
        - Start planning your move!

        Thank you for choosing Castle Apartments.

        Best regards,
        Castle Apartments Team
        """
    elif status == 'Rejected':
        message = f"""
        Dear {offer.user.first_name or offer.user.username},

        We're sorry to inform you that your offer of {offer.get_formatted_price()} for the property "{offer.property_name}" has been REJECTED.

        Don't be discouraged! We have many other great properties available. 
        Keep browsing our listings to find your perfect home.

        Best regards,
        Castle Apartments Team
        """
    else:  # For other statuses like 'Contingent'
        message = f"""
        Dear {offer.user.first_name or offer.user.username},

        The status of your offer of {offer.get_formatted_price()} for the property "{offer.property_name}" has been updated to {status}.

        Please log into your Castle Apartments account for more details.

        Best regards,
        Castle Apartments Team
        """

    # Store email in database
    email_record = Email.objects.create(
        buyer=buyer_email,
        seller=offer.seller.email if offer.seller and offer.seller.email else settings.EMAIL_HOST_USER,
        subject=subject,
        message=message
    )

    # Send the email
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[buyer_email],
        fail_silently=False,
    )

    return True

