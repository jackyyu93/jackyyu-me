import re

path = 'src/pages/index.astro'
with open(path) as f:
    s = f.read()

# ============ 1. HERO SUMMARY ============
old_hero_p = '''Force multiplier and seasoned Technical leader with 8+ years leading digital transformation, driving AI and enterprise initiatives, and building the foundations that let world-class teams move fast and deliver at scale.'''
new_hero_p = '''Force multiplier and seasoned Technical leader bridging strategy and execution at the highest levels of leadership. Translating organizational vision into action, driving AI and enterprise initiatives, and building the foundations that let world-class teams move fast and deliver at scale.'''
assert old_hero_p in s, "FAIL: hero paragraph not found"
s = s.replace(old_hero_p, new_hero_p)
print("✓ Hero summary updated")

# ============ 2. ROTATING WORD: ADD "product" ============
# Find the rotating word array in the JS — usually defined as ['operations', 'engineering', ...]
m_rot = re.search(r"const\s+words\s*=\s*\[([^\]]+)\]", s)
if m_rot:
    old_arr = m_rot.group(0)
    inner = m_rot.group(1)
    if "'product'" not in inner and '"product"' not in inner:
        # Add 'product' to the array. Detect quote style.
        new_inner = inner.rstrip().rstrip(',') + ", 'product'"
        new_arr = old_arr.replace(inner, new_inner)
        s = s.replace(old_arr, new_arr)
        print("✓ 'product' added to rotating word array")
    else:
        print("✓ 'product' already in rotating word array")
else:
    print("⚠ Rotating word array not found — may have a different structure. Check JS block manually.")

# ============ 3. ABOUT PROSE ============
old_about_prose = '''              <p>
                I&rsquo;m an executive operator and tech leader who thrives at the intersection of strategy, AI innovation, and organizational leadership. My 8+ years of experience spans integrating cutting edge AI acquisitions and bootstrapping the Core Cyber AI division at Cloudflare, leading digital transformation at Straumann Group, and overhauling operational excellence at FedEx. I previously led a life as an Industrial Engineer where I leaned into Lean, specializing in always improving and continually getting better.
              </p>
              <p>
                A few things I care about deeply: fostering great relationships and building high performing teams, understanding the &ldquo;Why&rdquo; to drive the &ldquo;How,&rdquo; and moving fast in environments where clarity and outcomes are more valuable than process. As AI transforms the digital landscape, I focus my efforts on how to deliver value in an era where the baseline capabilities of software are changing quickly.
              </p>'''

new_about_prose = '''              <p>
                I thrive at the intersection of strategy, AI innovation, and organizational leadership. My 8+ years of experience spans integrating cutting edge AI acquisitions at Cloudflare, driving digital transformation at Straumann Group, executing capital projects at Atmos Energy, and leading operational excellence at FedEx Express.
              </p>
              <p>
                A few things I care about deeply: fostering great relationships and building high performing teams, understanding the &ldquo;Why&rdquo; to drive the &ldquo;How,&rdquo; and moving fast in environments where clarity and outcomes are more valuable than process. As AI transforms the digital landscape, I focus my efforts on how to deliver value in an era where the baseline capabilities of software are changing quickly.
              </p>'''

assert old_about_prose in s, "FAIL: About prose not found"
s = s.replace(old_about_prose, new_about_prose)
print("✓ About prose updated")

# ============ 4. FUN FACTS: REMOVE "Born in China" ============
old_china = '''
              <li><p class="font-serif text-sm leading-snug" style="color: var(--text);">Born in China <span class="text-xs text-stone-500 font-mono">(ask me where!)</span></p></li>'''
assert old_china in s, "FAIL: Born in China line not found"
s = s.replace(old_china, '')
print("✓ 'Born in China' removed from Fun Facts")

# ============ 5. REORDER: MOVE PRINCIPLES UP, AFTER ABOUT ============
# Extract the entire Principles section block
principles_pattern = re.compile(
    r'\n\s*<!-- § 05 PRINCIPLES -->.*?</section>\n',
    re.DOTALL
)
m_p = principles_pattern.search(s)
assert m_p, "FAIL: Principles section block not found"
principles_block = m_p.group(0)

# Remove Principles from current location
s = s[:m_p.start()] + s[m_p.end():]
print("✓ Principles removed from old location")

# Find Impact section marker and insert Principles right before it
impact_marker = '<!-- § 02 IMPACT -->'
# Wait — Impact is currently § 02. Let's verify current state by looking for it
# After edit6 + edit7, ordering was: About §01, Impact §02, Work §03, Experience §04, Principles §05, Contact §06
# So the comment marker for Impact should be <!-- § 02 IMPACT -->
if impact_marker not in s:
    # Try alternative if marker doesn't exist
    impact_marker_alt = '<section id="impact"'
    assert impact_marker_alt in s, "FAIL: Impact section anchor not found"
    # Inject before <section id="impact"
    s = s.replace(impact_marker_alt, principles_block.lstrip() + '\n      <section id="impact"', 1)
    # We need a cleaner insertion — fall through and renumber later anyway
    print("✓ Principles inserted before Impact (via section anchor)")
else:
    s = s.replace(impact_marker, principles_block.strip() + '\n\n      ' + impact_marker, 1)
    print("✓ Principles inserted before Impact")

# ============ 6. RENUMBER ALL SECTION LABELS + COMMENT MARKERS ============
# New target order:
# § 01 About (unchanged)
# § 02 Principles (was § 05)
# § 03 Impact (was § 02)
# § 04 Selected Work (was § 03)
# § 05 Experience (was § 04)
# § 06 Contact (unchanged)

# Use temporary placeholders to avoid double-rename collisions
renumbers = [
    ('§ 05 — Principles', '§§§PRIN§§§'),
    ('<!-- § 05 PRINCIPLES -->', '<!--§§§PRIN§§§-->'),
    ('§ 02 — Impact', '§§§IMP§§§'),
    ('<!-- § 02 IMPACT -->', '<!--§§§IMP§§§-->'),
    ('§ 03 — Selected Work', '§§§WORK§§§'),
    ('<!-- § 03 SELECTED WORK -->', '<!--§§§WORK§§§-->'),
    ('§ 04 — Experience', '§§§EXP§§§'),
    ('<!-- § 04 EXPERIENCE -->', '<!--§§§EXP§§§-->'),
]

for old, placeholder in renumbers:
    if old in s:
        s = s.replace(old, placeholder)

# Now substitute placeholders with final numbers
finals = [
    ('§§§PRIN§§§', '§ 02 — Principles'),
    ('<!--§§§PRIN§§§-->', '<!-- § 02 PRINCIPLES -->'),
    ('§§§IMP§§§', '§ 03 — Impact'),
    ('<!--§§§IMP§§§-->', '<!-- § 03 IMPACT -->'),
    ('§§§WORK§§§', '§ 04 — Selected Work'),
    ('<!--§§§WORK§§§-->', '<!-- § 04 SELECTED WORK -->'),
    ('§§§EXP§§§', '§ 05 — Experience'),
    ('<!--§§§EXP§§§-->', '<!-- § 05 EXPERIENCE -->'),
]
for placeholder, final in finals:
    s = s.replace(placeholder, final)

print("✓ All sections renumbered")

# ============ 7. ADD PRINCIPLES TO NAV (between About and Impact) ============
if '#principles' not in s:
    old_nav = '<a href="#about" class="nav-link">About</a>\n          <a href="#impact" class="nav-link">Impact</a>'
    new_nav = '<a href="#about" class="nav-link">About</a>\n          <a href="#principles" class="nav-link">Principles</a>\n          <a href="#impact" class="nav-link">Impact</a>'
    assert old_nav in s, "FAIL: About → Impact nav link block not found"
    s = s.replace(old_nav, new_nav)
    print("✓ Principles nav link added")
else:
    # Already exists — reposition between About and Impact
    s = re.sub(r'\s*<a href="#principles"[^>]*>Principles</a>', '', s)
    old_nav = '<a href="#about" class="nav-link">About</a>\n          <a href="#impact" class="nav-link">Impact</a>'
    new_nav = '<a href="#about" class="nav-link">About</a>\n          <a href="#principles" class="nav-link">Principles</a>\n          <a href="#impact" class="nav-link">Impact</a>'
    if old_nav in s:
        s = s.replace(old_nav, new_nav)
        print("✓ Principles nav link repositioned")

# ============ 8. EXPERIENCE: ADD HUMAN INTEREST AT TOP + UPDATE CLOUDFLARE ============

# Find the Cloudflare experience block. The current top entry is Cloudflare 2025—Present.
# We need to: (a) insert Human Interest above it, (b) change Core Cyber AI sub-role to 2026 — 2026
# First, find the Cloudflare card opening marker

# Look for the pattern matching the current Cloudflare role block
old_cf_block = '''        <article class="border-t border-stone-800 pt-8 grid grid-cols-1 md:grid-cols-[12rem_1fr] gap-6 md:gap-12">
          <div class="space-y-3">
            <div class="experience-logo w-16 h-16 rounded flex items-center justify-center overflow-hidden">
              <img src="/logos/cloudflare.png" alt="Cloudflare logo" class="w-full h-full object-contain" />
            </div>
            <p class="text-xs tracking-widest text-stone-500 uppercase font-mono">
              2025 — PRESENT
            </p>
          </div>'''

# We're not editing the Cloudflare card structure — just the dates inside it.
# Update Core Cyber AI dates: "2026 — Present" → "2026 — 2026"
old_cyber = 'Core Cyber AI 2026 — Present'
new_cyber = 'Core Cyber AI 2026 — 2026'
if old_cyber in s:
    s = s.replace(old_cyber, new_cyber)
    print("✓ Core Cyber AI dates updated 2026 — 2026")
else:
    # Maybe formatting differs; try simpler markers
    alt_cyber = re.search(r'(Core Cyber AI[^<]*?)2026\s*[—-]\s*Present', s)
    if alt_cyber:
        s = s[:alt_cyber.start()] + alt_cyber.group(1) + '2026 — 2026' + s[alt_cyber.end():]
        print("✓ Core Cyber AI dates updated 2026 — 2026 (regex match)")
    else:
        print("⚠ Could not find 'Core Cyber AI ... Present' to update — check Experience section manually")

# Insert Human Interest article BEFORE the Cloudflare article block
# We need to find where Cloudflare's <article> starts and inject above it
# Look for the first <article> after the Experience section header

# Find "<!-- § 05 EXPERIENCE -->" (after renumbering) and locate the next <article>
exp_section_marker = '<!-- § 05 EXPERIENCE -->'
exp_idx = s.find(exp_section_marker)
assert exp_idx >= 0, "FAIL: Experience section marker not found after renumbering"

# Find first <article in Experience
article_idx = s.find('<article', exp_idx)
assert article_idx >= 0, "FAIL: First experience article not found"

# Look back for the indentation of that article line
line_start = s.rfind('\n', 0, article_idx) + 1
indent = s[line_start:article_idx]

human_interest_block = f'''{indent}<article class="border-t border-stone-800 pt-8 grid grid-cols-1 md:grid-cols-[12rem_1fr] gap-6 md:gap-12">
{indent}  <div class="space-y-3">
{indent}    <div class="experience-logo w-16 h-16 rounded flex items-center justify-center overflow-hidden">
{indent}      <img src="/logos/human-interest.png" alt="Human Interest logo" class="w-full h-full object-contain" />
{indent}    </div>
{indent}    <p class="text-xs tracking-widest text-stone-500 uppercase font-mono">
{indent}      2026 — PRESENT
{indent}    </p>
{indent}  </div>
{indent}  <div class="space-y-2">
{indent}    <h3 class="text-2xl md:text-3xl font-serif">Human Interest</h3>
{indent}    <p class="text-xs tracking-widest text-stone-500 uppercase font-mono">
{indent}      FinTech · Retirement Plans
{indent}    </p>
{indent}    <p class="text-stone-300 text-sm leading-relaxed pt-2">
{indent}      Technical Program Manager
{indent}    </p>
{indent}  </div>
{indent}</article>

{indent}'''

s = s[:article_idx] + human_interest_block + s[article_idx:]
print("✓ Human Interest article inserted at top of Experience")

# ============ WRITE FILE ============
with open(path, 'w') as f:
    f.write(s)
print("")
print("DONE — all changes applied.")
print("")
print("NEXT: drop a Human Interest logo at public/logos/human-interest.png")