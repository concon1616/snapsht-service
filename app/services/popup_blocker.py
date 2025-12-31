"""
Comprehensive Popup/Modal Blocker for Screenshot Service

Blocks:
- Email Service Provider (ESP) popups: Klaviyo, Mailchimp, Omnisend, Sendlane, etc.
- E-commerce platform modals: Square, Shopify, BigCommerce
- Cookie consent banners
- Chat widgets
- Newsletter signup forms
- Generic modal/popup patterns
"""

# =============================================================================
# ESP (Email Service Provider) Selectors
# =============================================================================

KLAVIYO_SELECTORS = [
    '.klaviyo-form',
    '[id^="klaviyo-form"]',
    '.klaviyo-popup',
    '.klaviyo_modal',
    '.klaviyo_inner',
    '.klaviyo_close_modal',
    '[class*="klaviyo"]',
    'div[data-testid="klaviyo-form"]',
]

MAILCHIMP_SELECTORS = [
    '#mc_embed_signup',
    '#mc-embedded-subscribe-form',
    '.mc-field-group',
    '#mce-responses',
    '.mc-modal',
    '[class*="mailchimp"]',
    '.mc_embed_signup',
    '#mc_embed_shell',
    '.mc-closeModal',
    '[id*="mc-embedded"]',
]

OMNISEND_SELECTORS = [
    '[class*="omnisend"]',
    '#omnisend-form',
    '.omnisend-popup',
    '.omnisend-form-container',
    '[data-omnisend]',
    'iframe[src*="omnisend"]',
]

SENDLANE_SELECTORS = [
    '.slf-widget__close-button',
    '.slf-button',
    '.form-element',
    '.form-element__text-element',
    '[class*="sendlane"]',
    '.slf-form',
    '.slf-widget',
    'iframe[src*="sendlane"]',
]

PRIVY_SELECTORS = [
    '[class*="privy"]',
    '#privy-popup',
    '.privy-popup-content',
    '.privy-popup-overlay',
    'iframe[src*="privy"]',
    '[data-privy]',
]

JUSTUNO_SELECTORS = [
    '[class*="justuno"]',
    '#justuno',
    '.justuno-popup',
    'iframe[src*="justuno"]',
    '[data-justuno]',
]

OPTINMONSTER_SELECTORS = [
    '[class*="optinmonster"]',
    '.om-holder',
    '.om-monster',
    '#om-holder',
    '[id*="om-"]',
    'iframe[src*="optinmonster"]',
    '.om-trigger-close',
]

SUMO_SELECTORS = [
    '[class*="sumome"]',
    '#sumome-smartbar',
    '.sumome-smartbar',
    '.sumome-react-wysiwyg',
    'iframe[src*="sumo"]',
    '[data-sumome]',
]

HUBSPOT_POPUP_SELECTORS = [
    '.leadinModal',
    '#leadinModal-preview',
    '.leadinModal-content',
    '.leadin-preview-wrapper',
    '[class*="hs-form"]',
    '.hs-form-iframe',
]

DRIP_SELECTORS = [
    '[class*="drip"]',
    '.drip-tab',
    '.drip-lightbox',
    '.drip-popup',
    'iframe[src*="getdrip"]',
]

CONVERTKIT_SELECTORS = [
    '[class*="convertkit"]',
    '.ck-modal',
    '.ck-form',
    '#convertkit-modal',
    'iframe[src*="convertkit"]',
]

AWEBER_SELECTORS = [
    '[class*="aweber"]',
    '.af-form',
    '#af-form',
    'iframe[src*="aweber"]',
]

CONSTANT_CONTACT_SELECTORS = [
    '[class*="ctct"]',
    '.ctct-form-embed',
    '.ctct-inline-form',
    'iframe[src*="constantcontact"]',
]

GETRESPONSE_SELECTORS = [
    '[class*="getresponse"]',
    '.gr-form',
    '#getresponse-form',
    'iframe[src*="getresponse"]',
]

ACTIVECAMPAIGN_SELECTORS = [
    '[class*="activecampaign"]',
    '._form',
    '[class*="_form"]',
    'iframe[src*="activehosted"]',
]

WHEELIO_SELECTORS = [
    '[class*="wheelio"]',
    '#wheelio',
    '.wheelio-popup',
    '.wheelio-wheel',
    'iframe[src*="wheelio"]',
]

SPIN_WHEEL_SELECTORS = [
    '[class*="spin-wheel"]',
    '[class*="spinwheel"]',
    '[class*="wheel-popup"]',
    '.spin-to-win',
    '.spin-a-sale',
    '[class*="fortune-wheel"]',
    '[class*="lucky-wheel"]',
]

# =============================================================================
# E-commerce Platform Selectors
# =============================================================================

SQUARE_SELECTORS = [
    '[class*="sq-"] [role="dialog"]',
    '[aria-label*="Sign in"]',
    '[aria-label*="sign up"]',
    '.sq-modal',
    '[class*="square-market"]',
    'div[role="dialog"][aria-modal="true"]',
    # Square Online specific
    '.market-login-modal',
    '.market-popup',
]

SHOPIFY_POPUP_SELECTORS = [
    '.shopify-popup',
    '[class*="shopify-popup"]',
    '.shopify-section-popup',
    '#shopify-pc__banner',
    '.shopify-challenge',
    '[data-shopify-popup]',
]

BIGCOMMERCE_SELECTORS = [
    '[class*="bigcommerce"]',
    '.bc-modal',
    '#bc-popup',
]

WOOCOMMERCE_SELECTORS = [
    '[class*="woocommerce-popup"]',
    '.wc-popup',
    '#woocommerce-popup',
]

# =============================================================================
# Newsletter/Signup Generic Patterns
# =============================================================================

NEWSLETTER_SELECTORS = [
    # Newsletter specific
    '[class*="newsletter"]',
    '[id*="newsletter"]',
    '[class*="Newsletter"]',
    '[id*="Newsletter"]',
    '.newsletter-popup',
    '.newsletter-modal',
    '.newsletter-signup',
    '#newsletter-signup',
    '.newsletter-widget',
    '#newsLetterSignUp',

    # Email signup
    '[class*="email-signup"]',
    '[class*="email-popup"]',
    '[class*="emailSignup"]',
    '[class*="emailPopup"]',
    '.email-capture',
    '.email-capture-popup',

    # Subscribe
    '[class*="subscribe-popup"]',
    '[class*="subscribe-modal"]',
    '[class*="subscription-popup"]',
    '.subscribe-popup',
    '.subscribe-modal',

    # Optin
    '[class*="optin"]',
    '[class*="opt-in"]',
    '.optin-popup',
    '.optin-modal',

    # Lead capture
    '[class*="lead-capture"]',
    '[class*="leadCapture"]',
    '.lead-popup',
    '.lead-modal',

    # Exit intent
    '[class*="exit-intent"]',
    '[class*="exitIntent"]',
    '.exit-popup',
    '.exit-modal',
]

# =============================================================================
# Generic Modal/Popup Patterns
# =============================================================================

GENERIC_MODAL_SELECTORS = [
    # Modal patterns
    '.modal-overlay',
    '.modal-backdrop',
    '.modal-wrapper',
    '[class*="modal-overlay"]',
    '[class*="modal-backdrop"]',
    '[class*="modalOverlay"]',
    '[class*="modalBackdrop"]',

    # Popup patterns
    '.popup-overlay',
    '.popup-wrapper',
    '.popup-container',
    '[class*="popup-overlay"]',
    '[class*="popupOverlay"]',

    # Lightbox
    '[class*="lightbox"]',
    '.fancybox-overlay',
    '.featherlight',

    # Dialog
    '[role="dialog"][aria-modal="true"]',
    '[role="alertdialog"]',

    # Overlay
    '.overlay-modal',
    '.page-overlay',
    '[class*="overlay"][class*="modal"]',
]

# =============================================================================
# Cookie/Consent Banners (Enhanced from dp-screenshots)
# =============================================================================

COOKIE_BANNER_SELECTORS = [
    # Consent Management Platforms
    '#onetrust-consent-sdk',
    '#onetrust-banner-sdk',
    '#CybotCookiebotDialog',
    '#CybotCookiebotDialogBody',
    '.cc-window',
    '.cc-banner',
    '#cookie-law-info-bar',
    '#hs-eu-cookie-confirmation',
    '.qc-cmp-ui-container',
    '#sp-cc',
    '.fc-consent-root',
    '#usercentrics-root',
    '.optanon-alert-box-wrapper',
    '[id*="tarteaucitron"]',
    '.cmp-root',
    '#gdpr-consent-tool-wrapper',
    '#cookie-notice',
    '#cookieNotice',
    '.cookie-notice',
    '.cookieNotice',
    '#didomi-host',
    '.didomi-popup-container',
    '#truste-consent-track',
    '#cmplz-cookiebanner-container',

    # Generic patterns
    '[class*="cookie-banner"]',
    '[class*="cookie-consent"]',
    '[class*="cookie-notice"]',
    '[class*="cookie-popup"]',
    '[class*="cookie-modal"]',
    '[class*="gdpr"]',
    '[class*="consent-banner"]',
    '[class*="privacy-banner"]',
    '[class*="CookieConsent"]',
    '[id*="cookie-banner"]',
    '[id*="cookie-consent"]',
    '[id*="cookie-notice"]',
    '[id*="gdpr"]',
    '[aria-label*="cookie"]',
    '[aria-label*="consent"]',
]

# =============================================================================
# Chat Widget Selectors
# =============================================================================

CHAT_WIDGET_SELECTORS = [
    # Intercom
    '#intercom-container',
    '.intercom-launcher',
    '.intercom-app',
    '.intercom-lightweight-app',

    # Drift
    '#drift-widget',
    '#drift-frame-controller',
    '.drift-frame-chat',

    # Crisp
    '.crisp-client',
    '#crisp-chatbox',

    # Zendesk
    '#launcher',
    '#webWidget',
    '[data-product="web_widget"]',

    # HubSpot
    '#hubspot-messages-iframe-container',

    # Tawk.to
    '.tawk-min-container',
    '#tawkchat-container',

    # LiveChat
    '#chat-widget-container',
    '#livechat-compact-container',

    # Tidio
    '#tidio-chat',
    '#tidio-chat-iframe',

    # Freshdesk
    '#freshdesk-widget',

    # Olark
    '#olark-wrapper',

    # Facebook Messenger
    '.fb-customerchat',
    '.fb_dialog',

    # Gorgias
    '#gorgias-chat-container',

    # Generic
    '[class*="chat-widget"]',
    '[class*="chatWidget"]',
    '[class*="chat-bubble"]',
    '[class*="chatBubble"]',
    '[id*="chat-widget"]',
    '[id*="chatWidget"]',
]

# =============================================================================
# Social Proof/FOMO Popups
# =============================================================================

SOCIAL_PROOF_SELECTORS = [
    '[class*="fomo"]',
    '[class*="social-proof"]',
    '[class*="socialProof"]',
    '[class*="proof-popup"]',
    '[class*="recent-sales"]',
    '[class*="recentSales"]',
    '[class*="live-visitor"]',
    '[class*="liveVisitor"]',
    '.nudgify',
    '.proof-widget',
    '#fomo-notification',
]

# =============================================================================
# Close Button Selectors (for clicking to dismiss)
# =============================================================================

CLOSE_BUTTON_SELECTORS = [
    # Standard close buttons
    '[class*="close"]',
    '[class*="Close"]',
    '[aria-label*="close"]',
    '[aria-label*="Close"]',
    '[aria-label*="dismiss"]',
    '[aria-label*="Dismiss"]',

    # X buttons
    '.close-btn',
    '.close-button',
    '.btn-close',
    '.modal-close',
    '.popup-close',
    '.dialog-close',

    # Data attributes
    '[data-dismiss="modal"]',
    '[data-close]',
    '[data-dismiss]',

    # SVG/Icon close buttons
    'button[aria-label="Close"]',
    'button[aria-label="close"]',
    'button.close',
    '.icon-close',
    '.icon-x',

    # Specific patterns
    '.klaviyo-close',
    '.om-trigger-close',
    '.mc-closeModal',
]

# =============================================================================
# Domains to Block (for request interception)
# =============================================================================

ESP_DOMAINS = [
    # Klaviyo
    'static.klaviyo.com',
    'a.klaviyo.com',
    'klaviyo.com',

    # Mailchimp
    'chimpstatic.com',
    'list-manage.com',
    'mailchimp.com',
    'mcusercontent.com',

    # Omnisend
    'omnisend.com',
    'omnisrc.com',

    # Sendlane
    'sendlane.com',

    # Privy
    'privy.com',
    'privymktg.com',

    # Justuno
    'justuno.com',
    'cdn.justuno.com',

    # OptinMonster
    'optinmonster.com',
    'optmstr.com',

    # Sumo
    'sumo.com',
    'sumome.com',

    # Drip
    'getdrip.com',
    'drip.com',

    # ConvertKit
    'convertkit.com',
    'ck.page',

    # AWeber
    'aweber.com',

    # Constant Contact
    'constantcontact.com',
    'ctctcdn.com',

    # GetResponse
    'getresponse.com',

    # ActiveCampaign
    'activehosted.com',
    'activecampaign.com',

    # Wheelio & Spin Wheels
    'wheelio.com',
    'wheelpop.com',
    'spinwheel.io',
]

# =============================================================================
# Combined Selector Lists
# =============================================================================

ALL_ESP_SELECTORS = (
    KLAVIYO_SELECTORS +
    MAILCHIMP_SELECTORS +
    OMNISEND_SELECTORS +
    SENDLANE_SELECTORS +
    PRIVY_SELECTORS +
    JUSTUNO_SELECTORS +
    OPTINMONSTER_SELECTORS +
    SUMO_SELECTORS +
    HUBSPOT_POPUP_SELECTORS +
    DRIP_SELECTORS +
    CONVERTKIT_SELECTORS +
    AWEBER_SELECTORS +
    CONSTANT_CONTACT_SELECTORS +
    GETRESPONSE_SELECTORS +
    ACTIVECAMPAIGN_SELECTORS +
    WHEELIO_SELECTORS +
    SPIN_WHEEL_SELECTORS
)

ALL_ECOMMERCE_SELECTORS = (
    SQUARE_SELECTORS +
    SHOPIFY_POPUP_SELECTORS +
    BIGCOMMERCE_SELECTORS +
    WOOCOMMERCE_SELECTORS
)

ALL_POPUP_SELECTORS = (
    ALL_ESP_SELECTORS +
    ALL_ECOMMERCE_SELECTORS +
    NEWSLETTER_SELECTORS +
    GENERIC_MODAL_SELECTORS +
    COOKIE_BANNER_SELECTORS +
    CHAT_WIDGET_SELECTORS +
    SOCIAL_PROOF_SELECTORS
)


def generate_hiding_css(selectors: list) -> str:
    """Generate CSS to hide elements matching the given selectors."""
    return '\n'.join([
        f'{selector} {{ display: none !important; visibility: hidden !important; opacity: 0 !important; pointer-events: none !important; }}'
        for selector in selectors
    ])


def get_popup_dismiss_script() -> str:
    """
    Generate JavaScript to aggressively find and dismiss popups.
    Uses multiple strategies: clicking close buttons, hiding elements, and heuristic detection.
    """
    return '''
    (function() {
        // Strategy 1: Click close buttons
        const closeSelectors = [
            '[class*="close"]', '[class*="Close"]',
            '[aria-label*="close"]', '[aria-label*="Close"]',
            '[aria-label*="dismiss"]', '[aria-label*="Dismiss"]',
            '[class*="dismiss"]', '[class*="Dismiss"]',
            '.close-btn', '.close-button', '.btn-close',
            '.modal-close', '.popup-close', '.dialog-close',
            '[data-dismiss="modal"]', '[data-close]', '[data-dismiss]',
            'button[aria-label="Close"]', 'button[aria-label="close"]',
            'button.close', '.icon-close', '.icon-x',
            // ESP specific
            '.klaviyo-close', '.om-trigger-close', '.mc-closeModal',
            '.slf-widget__close-button', '.privy-close',
            // X symbol buttons
            'button:has(svg)', 'button:has(.icon)',
        ];

        for (const selector of closeSelectors) {
            try {
                const elements = document.querySelectorAll(selector);
                elements.forEach(el => {
                    // Check if element is visible
                    if (el.offsetParent !== null && el.offsetWidth > 0) {
                        // Check if inside a modal/popup
                        const parent = el.closest('[class*="modal"], [class*="popup"], [class*="klaviyo"], [class*="overlay"], [role="dialog"]');
                        if (parent) {
                            el.click();
                        }
                    }
                });
            } catch (e) {}
        }

        // Strategy 2: Hide known popup containers
        const hideSelectors = ''' + str(ALL_POPUP_SELECTORS) + ''';

        for (const selector of hideSelectors) {
            try {
                document.querySelectorAll(selector).forEach(el => {
                    el.style.setProperty('display', 'none', 'important');
                    el.style.setProperty('visibility', 'hidden', 'important');
                    el.style.setProperty('opacity', '0', 'important');
                });
            } catch (e) {}
        }

        // Strategy 3: Hide overlays and backdrops
        const overlaySelectors = [
            '[class*="overlay"]', '[class*="backdrop"]',
            '[class*="Overlay"]', '[class*="Backdrop"]',
            '.modal-backdrop', '.popup-overlay',
        ];

        for (const selector of overlaySelectors) {
            try {
                document.querySelectorAll(selector).forEach(el => {
                    const style = window.getComputedStyle(el);
                    // Only hide if it's positioned fixed/absolute with high z-index
                    if ((style.position === 'fixed' || style.position === 'absolute') &&
                        parseInt(style.zIndex || '0') > 100) {
                        el.style.setProperty('display', 'none', 'important');
                    }
                });
            } catch (e) {}
        }

        // Strategy 4: Heuristic detection - hide fixed/sticky elements with popup keywords
        const popupKeywords = [
            'popup', 'modal', 'overlay', 'newsletter', 'subscribe', 'signup',
            'sign-up', 'email', 'klaviyo', 'mailchimp', 'omnisend', 'privy',
            'justuno', 'optin', 'opt-in', 'lead', 'capture', 'exit', 'discount',
            'coupon', 'spin', 'wheel', 'fomo', 'social-proof', 'notification'
        ];

        document.querySelectorAll('div, section, aside, dialog, [role="dialog"]').forEach(el => {
            const style = window.getComputedStyle(el);
            const isFixed = style.position === 'fixed' || style.position === 'sticky';
            const isHighZ = parseInt(style.zIndex || '0') > 999;

            if (isFixed || isHighZ) {
                const classList = Array.from(el.classList).join(' ').toLowerCase();
                const id = (el.id || '').toLowerCase();
                const hasKeyword = popupKeywords.some(kw =>
                    classList.includes(kw) || id.includes(kw)
                );

                if (hasKeyword) {
                    el.style.setProperty('display', 'none', 'important');
                    el.style.setProperty('visibility', 'hidden', 'important');
                }
            }
        });

        // Strategy 5: Remove iframes from ESP domains
        const espDomains = ''' + str(ESP_DOMAINS) + ''';

        document.querySelectorAll('iframe').forEach(iframe => {
            const src = iframe.src || '';
            if (espDomains.some(domain => src.includes(domain))) {
                iframe.style.setProperty('display', 'none', 'important');
            }
        });

        // Strategy 6: Re-enable scrolling on body
        document.body.style.overflow = 'auto';
        document.body.style.position = 'static';
        document.documentElement.style.overflow = 'auto';
        document.documentElement.style.position = 'static';

        // Remove any scroll locks
        document.body.classList.remove('modal-open', 'no-scroll', 'overflow-hidden');
        document.documentElement.classList.remove('modal-open', 'no-scroll', 'overflow-hidden');

    })();
    '''


def get_enhanced_popup_dismiss_script() -> str:
    """
    More aggressive popup dismissal with mutation observer for dynamically loaded popups.
    """
    return '''
    (function() {
        // Initial cleanup
        ''' + get_popup_dismiss_script() + '''

        // Set up mutation observer for dynamically loaded popups
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                mutation.addedNodes.forEach((node) => {
                    if (node.nodeType === 1) { // Element node
                        const el = node;
                        const classList = Array.from(el.classList || []).join(' ').toLowerCase();
                        const id = (el.id || '').toLowerCase();

                        const popupPatterns = ['popup', 'modal', 'overlay', 'klaviyo', 'mailchimp',
                                               'omnisend', 'privy', 'optin', 'newsletter', 'subscribe'];

                        if (popupPatterns.some(p => classList.includes(p) || id.includes(p))) {
                            el.style.setProperty('display', 'none', 'important');
                        }
                    }
                });
            });
        });

        observer.observe(document.body, { childList: true, subtree: true });

        // Stop observing after 5 seconds
        setTimeout(() => observer.disconnect(), 5000);
    })();
    '''
