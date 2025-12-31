# Comprehensive Popup/Modal Blocking Plan

## Overview

This document outlines all major ESPs (Email Service Providers), popup tools, and e-commerce marketing platforms that need to be blocked for clean screenshot/video capture, along with technical strategies for handling edge cases.

---

## 1. Major ESPs (Email Service Providers)

### Tier 1 - Most Common (High Priority)

| Provider | Domain Patterns | Known Selectors | Status |
|----------|-----------------|-----------------|--------|
| **Klaviyo** | `klaviyo.com`, `static.klaviyo.com`, `a.klaviyo.com` | `.klaviyo-form`, `[id^="klaviyo-form"]`, `[class*="klaviyo"]` | ✅ Implemented |
| **Mailchimp** | `mailchimp.com`, `chimpstatic.com`, `list-manage.com` | `#mc_embed_signup`, `.mc-modal`, `[class*="mailchimp"]` | ✅ Implemented |
| **Omnisend** | `omnisend.com`, `omnisrc.com` | `[class*="omnisend"]`, `#omnisend-form` | ✅ Implemented |
| **Attentive** | `cdn.attn.tv`, `attn.tv` | `[class*="attentive"]`, `__attentive_*` cookies | ⚠️ Needs Testing |
| **Privy** | `privy.com`, `privymktg.com` | `[class*="privy"]`, `#privy-popup` | ✅ Implemented |

### Tier 2 - Common

| Provider | Domain Patterns | Known Selectors | Status |
|----------|-----------------|-----------------|--------|
| **Sendlane** | `sendlane.com` | `.slf-widget`, `[class*="sendlane"]` | ✅ Implemented |
| **ActiveCampaign** | `activehosted.com`, `activecampaign.com` | `._form`, `[class*="activecampaign"]` | ✅ Implemented |
| **HubSpot** | `hubspot.com`, `hs-scripts.com`, `hsforms.com` | `.leadinModal`, `[class*="hs-form"]` | ✅ Implemented |
| **GetResponse** | `getresponse.com` | `.gr-form`, `[class*="getresponse"]` | ✅ Implemented |
| **ConvertKit** | `convertkit.com`, `ck.page` | `.ck-modal`, `[class*="convertkit"]` | ✅ Implemented |
| **Drip** | `getdrip.com`, `drip.com` | `.drip-tab`, `.drip-lightbox` | ✅ Implemented |
| **AWeber** | `aweber.com` | `.af-form`, `[class*="aweber"]` | ✅ Implemented |
| **Constant Contact** | `constantcontact.com`, `ctctcdn.com` | `.ctct-form-embed`, `[class*="ctct"]` | ✅ Implemented |

### Tier 3 - Enterprise/Specialized

| Provider | Domain Patterns | Notes |
|----------|-----------------|-------|
| **Brevo (Sendinblue)** | `brevo.com`, `sendinblue.com` | Forms typically embedded |
| **Campaign Monitor** | `campaignmonitor.com` | Less common popups |
| **Moosend** | `moosend.com` | Growing platform |
| **MailerLite** | `mailerlite.com` | Popular with small businesses |

---

## 2. Popup/Modal Tools

### Tier 1 - Most Common (High Priority)

| Tool | Domain Patterns | Known Selectors | Status |
|------|-----------------|-----------------|--------|
| **OptinMonster** | `optinmonster.com`, `optmstr.com` | `.om-holder`, `[id*="om-"]`, `.om-monster` | ✅ Implemented |
| **Justuno** | `justuno.com`, `cdn.justuno.com` | `[class*="justuno"]`, `#justuno` | ✅ Implemented |
| **Sumo/SumoMe** | `sumo.com`, `sumome.com` | `[class*="sumome"]`, `#sumome-smartbar` | ✅ Implemented |
| **Privy** | (see ESPs above) | (see ESPs above) | ✅ Implemented |
| **OptiMonk** | `optimonk.com` | `[class*="optimonk"]`, `.om-popup` | ❌ Not Implemented |

### Tier 2 - Common

| Tool | Domain Patterns | Known Selectors | Status |
|------|-----------------|-----------------|--------|
| **Wisepops** | `wisepops.com` | `[class*="wisepops"]` | ❌ Not Implemented |
| **Poptin** | `poptin.com` | `[class*="poptin"]` | ❌ Not Implemented |
| **Sleeknote** | `sleeknote.com` | `[class*="sleeknote"]` | ❌ Not Implemented |
| **Hello Bar** | `hellobar.com` | `#hellobar`, `[class*="hellobar"]` | ❌ Not Implemented |
| **Picreel** | `picreel.com` | `[class*="picreel"]` | ❌ Not Implemented |
| **Plerdy** | `plerdy.com` | `[class*="plerdy"]` | ❌ Not Implemented |

---

## 3. Gamification/Spin Wheel Tools

| Tool | Domain Patterns | Known Selectors | Status |
|------|-----------------|-----------------|--------|
| **Wheelio** | `wheelio.com` | `[class*="wheelio"]`, `#wheelio-container` | ✅ Implemented |
| **Spin-a-Sale** | Various | `.spin-a-sale`, `[class*="spin-a-sale"]` | ✅ Implemented |
| **WooHoo** | Shopify app | `[class*="woohoo"]` | ✅ Implemented |
| **SmashPops** | Shopify app | `[class*="smashpops"]` | ❌ Not Implemented |
| **Wheelify** | Shopify app | `[class*="wheelify"]` | ❌ Not Implemented |
| **PopSpin** | Shopify app | `[class*="popspin"]` | ❌ Not Implemented |
| **BuzzSubs** | Shopify app | `[class*="buzzsubs"]` | ❌ Not Implemented |
| **1Click Popups (1CP)** | Shopify app | `[class*="1cp"]`, `[class*="one-click"]` | ❌ Not Implemented |

---

## 4. E-commerce Platform Native Popups

| Platform | Known Selectors | Status |
|----------|-----------------|--------|
| **Square Online** | `.sq-modal`, `.market-login-modal` | ✅ Fixed |
| **Shopify** | `.shopify-popup`, `#shopify-pc__banner` | ✅ Implemented |
| **BigCommerce** | `.bc-modal`, `[class*="bigcommerce"]` | ✅ Implemented |
| **WooCommerce** | `.wc-popup`, `[class*="woocommerce-popup"]` | ✅ Implemented |
| **Squarespace** | Various (custom implementations) | ⚠️ Partial |
| **Wix** | Various (custom implementations) | ⚠️ Partial |

---

## 5. Chat Widgets (Already Implemented)

| Widget | Domain Patterns | Status |
|--------|-----------------|--------|
| Intercom | `intercom.com` | ✅ |
| Drift | `drift.com` | ✅ |
| Crisp | `crisp.chat` | ✅ |
| Zendesk | `zendesk.com` | ✅ |
| Tawk.to | `tawk.to` | ✅ |
| LiveChat | `livechat.com` | ✅ |
| Tidio | `tidio.com` | ✅ |
| Freshdesk | `freshdesk.com` | ✅ |
| Olark | `olark.com` | ✅ |
| Gorgias | `gorgias.io` | ✅ |
| Facebook Messenger | `facebook.com` | ✅ |
| HubSpot Chat | `hubspot.com` | ✅ |

---

## 6. Social Proof/FOMO Tools

| Tool | Domain Patterns | Known Selectors | Status |
|------|-----------------|-----------------|--------|
| **ProveSource** | `provesrc.com` | `[class*="provesource"]` | ⚠️ Partial |
| **Fomo** | `fomo.com` | `[class*="fomo"]` | ✅ Implemented |
| **Nudgify** | `nudgify.com` | `.nudgify`, `[class*="nudgify"]` | ⚠️ Partial |
| **TrustPulse** | `trustpulse.com` | `[class*="trustpulse"]` | ❌ Not Implemented |
| **Proof** | `useproof.com` | `[class*="proof"]` | ⚠️ Partial |

---

## 7. Technical Challenges & Solutions

### Challenge 1: Shadow DOM

**Problem**: Some popup providers use Shadow DOM to encapsulate their HTML/CSS, making it invisible to regular DOM queries.

**Detection**:
```javascript
// Check for shadow roots
document.querySelectorAll('*').forEach(el => {
    if (el.shadowRoot) {
        console.log('Shadow root found:', el);
    }
});
```

**Solution Strategy**:
```javascript
// Pierce shadow DOM to find and hide popups
function pierceAndHide(root = document) {
    const elements = root.querySelectorAll('*');
    elements.forEach(el => {
        // Check this element
        checkAndHidePopup(el);

        // Recurse into shadow roots
        if (el.shadowRoot) {
            pierceAndHide(el.shadowRoot);
        }
    });
}
```

**Implementation Status**: ❌ Not Implemented

---

### Challenge 2: Iframes

**Problem**: Popups loaded in iframes have their own document context.

**Detection**:
```javascript
// Find all iframes
document.querySelectorAll('iframe').forEach(iframe => {
    console.log('Iframe src:', iframe.src);
});
```

**Solution Strategies**:

1. **Hide iframe by src pattern** (Already implemented):
```javascript
const espDomains = ['klaviyo.com', 'privy.com', ...];
document.querySelectorAll('iframe').forEach(iframe => {
    if (espDomains.some(d => iframe.src.includes(d))) {
        iframe.style.display = 'none';
    }
});
```

2. **Access iframe content** (Same-origin only):
```javascript
document.querySelectorAll('iframe').forEach(iframe => {
    try {
        const iframeDoc = iframe.contentDocument || iframe.contentWindow.document;
        // Now can query inside iframe
        iframeDoc.querySelectorAll('.popup').forEach(el => el.remove());
    } catch (e) {
        // Cross-origin - can only hide the iframe itself
    }
});
```

3. **Block iframe loading via request interception** (Selenium/Puppeteer):
```python
# In Selenium with Chrome DevTools Protocol
driver.execute_cdp_cmd('Network.setBlockedURLs', {
    'urls': ['*klaviyo*', '*privy*', '*justuno*']
})
driver.execute_cdp_cmd('Network.enable', {})
```

**Implementation Status**: ⚠️ Partial (src pattern matching only)

---

### Challenge 3: Dynamically Loaded Popups

**Problem**: Popups often load after initial page render via JavaScript.

**Solution Strategies**:

1. **Extended wait time** (Current approach):
```python
await asyncio.sleep(3)  # Wait for popups to load
await dismiss_popups()
```

2. **MutationObserver** (Already implemented):
```javascript
const observer = new MutationObserver((mutations) => {
    mutations.forEach(m => {
        m.addedNodes.forEach(node => {
            if (isPopup(node)) hideElement(node);
        });
    });
});
observer.observe(document.body, { childList: true, subtree: true });
```

3. **Network request interception** (Better approach):
```python
# Block popup scripts from loading at all
driver.execute_cdp_cmd('Network.setBlockedURLs', {
    'urls': ['*klaviyo*', '*optinmonster*', ...]
})
```

**Implementation Status**: ⚠️ Partial (MutationObserver, but not network blocking)

---

### Challenge 4: CSS-only Detection Limitations

**Problem**: CSS `display: none` can't check element size, position, or content.

**Current Approach**: JavaScript-based detection with size checks.

**Better Approach**: Use JavaScript for all popup hiding, CSS only for known-safe selectors.

**Implementation Status**: ✅ Partially addressed (size check added)

---

### Challenge 5: Text Content Detection

**Problem**: Some popups don't have distinctive classes but contain recognizable text.

**Solution** (Partially implemented):
```javascript
const promoKeywords = ['spin to win', 'subscribe', 'newsletter', ...];
document.querySelectorAll('div').forEach(el => {
    const text = el.textContent.toLowerCase();
    if (promoKeywords.some(kw => text.includes(kw))) {
        if (isPositionedAsPopup(el) && !isTooLarge(el)) {
            el.style.display = 'none';
        }
    }
});
```

**Implementation Status**: ✅ Implemented

---

## 8. Implementation Roadmap

### Phase 1: Immediate (Current)
- [x] Core ESP selectors (Klaviyo, Mailchimp, Omnisend, etc.)
- [x] Core popup tool selectors (OptinMonster, Justuno, Privy, etc.)
- [x] Cookie banner blocking
- [x] Chat widget blocking
- [x] Basic spin wheel patterns
- [x] Size-based filtering (don't hide main content)
- [x] Text content detection

### Phase 2: Short-term
- [ ] Add missing popup providers (OptiMonk, Wisepops, Poptin, Sleeknote, etc.)
- [ ] Add missing spin wheel apps (SmashPops, Wheelify, PopSpin, etc.)
- [ ] Implement network request blocking for popup scripts
- [ ] Add Attentive-specific selectors
- [ ] Test on 50+ e-commerce sites

### Phase 3: Medium-term
- [ ] Shadow DOM piercing
- [ ] Cross-origin iframe handling improvements
- [ ] Machine learning-based popup detection
- [ ] Visual detection (fixed position + overlay pattern)
- [ ] Close button auto-detection and clicking

### Phase 4: Long-term
- [ ] Crowdsourced selector database
- [ ] Automatic selector discovery via site analysis
- [ ] Real-time popup detection API
- [ ] Browser extension for selector testing

---

## 9. Testing Sites

Sites known to have popups for testing:

| Site | Popup Provider | Type |
|------|----------------|------|
| colourpop.com | Unknown (Attentive?) | Spin wheel |
| fashionnova.com | Multiple | Newsletter |
| gymshark.com | Klaviyo | Newsletter |
| allbirds.com | Multiple | Newsletter |
| skims.com | Multiple | Newsletter |
| princesspolly.com | Multiple | Spin wheel |
| hellomolly.com | Wheelio? | Spin wheel |
| flickerfizz.com | Square Online | Login modal |

---

## 10. Resources

- [Fanboy's Annoyance List](https://easylist.to/easylist/fanboy-annoyance.txt) - Community filter list
- [Web Annoyances Ultralist](https://github.com/nicksheffield/webannoyances) - GitHub filter list
- [uBlock Origin Filters](https://github.com/gorhill/uBlock) - Browser extension filters
- [EasyList](https://github.com/easylist/easylist) - Ad blocking filter lists

---

## Changelog

- **2024-12-31**: Initial document created with comprehensive ESP/popup tool list
- **2024-12-31**: Added shadow DOM and iframe solutions
- **2024-12-31**: Added implementation roadmap
