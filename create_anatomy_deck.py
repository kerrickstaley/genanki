#!/usr/bin/env python3
"""
Comprehensive Anatomy Flashcard Deck Generator
Creates a thorough Anki deck for Unit 2: Hip, Knee, Ankle & Nervous System anatomy
Focuses on muscles, joints, movements, and clinical applications
"""

import genanki
import random

# Generate unique IDs for our models and deck
# Using random IDs as per genanki best practices
DECK_ID = 1847562934
BASIC_MODEL_ID = 1847562935
BASIC_REVERSE_MODEL_ID = 1847562936
CLOZE_MODEL_ID = 1847562937
CLINICAL_MODEL_ID = 1847562938
COMPARISON_MODEL_ID = 1847562939

# Custom CSS for better card appearance
CUSTOM_CSS = """
.card {
    font-family: Arial, sans-serif;
    font-size: 20px;
    text-align: center;
    color: #333;
    background-color: white;
    padding: 20px;
}

.front {
    font-size: 24px;
    font-weight: bold;
    color: #2c3e50;
    margin-bottom: 15px;
}

.back {
    font-size: 20px;
    color: #34495e;
    line-height: 1.6;
}

.tag {
    font-size: 14px;
    color: #7f8c8d;
    font-style: italic;
    margin-top: 15px;
}

.clinical {
    background-color: #ecf0f1;
    border-left: 4px solid #3498db;
    padding: 10px;
    margin: 10px 0;
}

.emphasis {
    color: #e74c3c;
    font-weight: bold;
}

ul {
    text-align: left;
    display: inline-block;
    margin: 10px auto;
}

li {
    margin: 5px 0;
}

.cloze {
    font-weight: bold;
    color: #3498db;
}

.nightMode .cloze {
    color: #5dade2;
}
"""

# Define custom models

# Model 1: Basic Question-Answer (One direction)
basic_model = genanki.Model(
    BASIC_MODEL_ID,
    'Anatomy Basic',
    fields=[
        {'name': 'Question'},
        {'name': 'Answer'},
        {'name': 'Tags'},
    ],
    templates=[
        {
            'name': 'Card 1',
            'qfmt': '<div class="front">{{Question}}</div>',
            'afmt': '<div class="front">{{Question}}</div><hr id="answer"><div class="back">{{Answer}}</div><div class="tag">{{Tags}}</div>',
        },
    ],
    css=CUSTOM_CSS
)

# Model 2: Basic with Reverse (Two direction cards)
basic_reverse_model = genanki.Model(
    BASIC_REVERSE_MODEL_ID,
    'Anatomy Basic (Reversed)',
    fields=[
        {'name': 'Front'},
        {'name': 'Back'},
        {'name': 'Tags'},
    ],
    templates=[
        {
            'name': 'Forward',
            'qfmt': '<div class="front">{{Front}}</div>',
            'afmt': '<div class="front">{{Front}}</div><hr id="answer"><div class="back">{{Back}}</div><div class="tag">{{Tags}}</div>',
        },
        {
            'name': 'Reverse',
            'qfmt': '<div class="front">{{Back}}</div>',
            'afmt': '<div class="front">{{Back}}</div><hr id="answer"><div class="back">{{Front}}</div><div class="tag">{{Tags}}</div>',
        },
    ],
    css=CUSTOM_CSS
)

# Model 3: Cloze Deletion
cloze_model = genanki.Model(
    CLOZE_MODEL_ID,
    'Anatomy Cloze',
    model_type=genanki.Model.CLOZE,
    fields=[
        {'name': 'Text'},
        {'name': 'Extra'},
        {'name': 'Tags'},
    ],
    templates=[
        {
            'name': 'Cloze',
            'qfmt': '{{cloze:Text}}',
            'afmt': '{{cloze:Text}}<br><div class="back">{{Extra}}</div><div class="tag">{{Tags}}</div>',
        },
    ],
    css=CUSTOM_CSS
)

# Model 4: Clinical Application (with additional context)
clinical_model = genanki.Model(
    CLINICAL_MODEL_ID,
    'Anatomy Clinical',
    fields=[
        {'name': 'Clinical Question'},
        {'name': 'Answer'},
        {'name': 'Context'},
        {'name': 'Tags'},
    ],
    templates=[
        {
            'name': 'Clinical Card',
            'qfmt': '<div class="clinical"><div class="front">{{Clinical Question}}</div></div>',
            'afmt': '<div class="clinical"><div class="front">{{Clinical Question}}</div></div><hr id="answer"><div class="back">{{Answer}}</div><div class="back" style="margin-top:10px; font-size:16px; color:#7f8c8d;">{{Context}}</div><div class="tag">{{Tags}}</div>',
        },
    ],
    css=CUSTOM_CSS
)

# Model 5: Comparison Cards (for distinguishing similar concepts)
comparison_model = genanki.Model(
    COMPARISON_MODEL_ID,
    'Anatomy Comparison',
    fields=[
        {'name': 'Concept'},
        {'name': 'Comparison'},
        {'name': 'Tags'},
    ],
    templates=[
        {
            'name': 'Comparison',
            'qfmt': '<div class="front">Compare and contrast:</div><div class="back" style="font-size:18px; margin-top:10px;">{{Concept}}</div>',
            'afmt': '<div class="front">Compare and contrast:</div><div class="back" style="font-size:18px; margin-top:10px;">{{Concept}}</div><hr id="answer"><div class="back">{{Comparison}}</div><div class="tag">{{Tags}}</div>',
        },
    ],
    css=CUSTOM_CSS
)

# Create the deck
deck = genanki.Deck(DECK_ID, 'Anatomy Unit 2: Muscles, Joints & Movements')

# ============================================================================
# CHAPTER 9: NECK AND TRUNK
# ============================================================================

# Neck Flexors - Basic Cards
deck.add_note(genanki.Note(
    model=basic_model,
    fields=[
        'What are the primary head/neck flexors?',
        '<ul><li>Sternocleidomastoid</li><li>Prevertebral group / Deep Cervical Flexors</li></ul>',
        'Chapter 9: Neck Flexors'
    ]
))

deck.add_note(genanki.Note(
    model=basic_reverse_model,
    fields=[
        'Sternocleidomastoid',
        'Bilateral: Neck flexion<br>Unilateral: Lateral flexion (same side), Rotation (opposite side)',
        'Chapter 9: Multi-action Muscle'
    ]
))

# Cloze cards for neck flexors
deck.add_note(genanki.Note(
    model=cloze_model,
    fields=[
        'The {{c1::sternocleidomastoid}} and {{c2::prevertebral group}} are the primary head and neck flexors.',
        '',
        'Chapter 9: Neck Flexors'
    ]
))

deck.add_note(genanki.Note(
    model=cloze_model,
    fields=[
        'When the sternocleidomastoid contracts {{c1::bilaterally}}, it produces {{c2::neck flexion}}. When it contracts {{c3::unilaterally}}, it produces lateral flexion to the {{c4::same side}} and rotation to the {{c5::opposite side}}.',
        '',
        'Chapter 9: SCM Actions'
    ]
))

# Head/Neck Extensors
deck.add_note(genanki.Note(
    model=basic_model,
    fields=[
        'What are the primary head/neck extensors?',
        '<ul><li>Splenii / Splenius Group</li><li>Erector spinae</li><li>Transversospinalis</li><li>Suboccipital group</li></ul>',
        'Chapter 9: Neck Extensors'
    ]
))

deck.add_note(genanki.Note(
    model=cloze_model,
    fields=[
        'The head and neck extensors include the {{c1::splenii}}, {{c2::erector spinae}}, {{c3::transversospinalis}}, and {{c4::suboccipital}} group.',
        '',
        'Chapter 9: Neck Extensors'
    ]
))

# Neck Lateral Flexors
deck.add_note(genanki.Note(
    model=basic_model,
    fields=[
        'What muscles perform lateral flexion of the neck?',
        '<ul><li>Sternocleidomastoid</li><li>Splenii / Splenius Group</li><li>Scalenes</li><li>Erector spinae</li></ul>',
        'Chapter 9: Neck Lateral Flexors'
    ]
))

deck.add_note(genanki.Note(
    model=cloze_model,
    fields=[
        'Neck lateral flexion is performed by {{c1::sternocleidomastoid}}, {{c2::splenii}}, {{c3::scalenes}}, and {{c4::erector spinae}}.',
        '',
        'Chapter 9: Neck Lateral Flexors'
    ]
))

# Neck Rotators - Same Side
deck.add_note(genanki.Note(
    model=basic_model,
    fields=[
        'Which neck muscles rotate to the SAME side?',
        '<ul><li>Splenii / Splenius Group</li><li>Obliquus capitis inferior (at AA joint)</li><li>Rectus capitis posterior major (at AO joint)</li></ul>',
        'Chapter 9: Same-Side Rotators'
    ]
))

deck.add_note(genanki.Note(
    model=cloze_model,
    fields=[
        'Same-side neck rotators include {{c1::splenii}}, {{c2::obliquus capitis inferior}} (at AA joint), and {{c3::rectus capitis posterior major}} (at AO joint).',
        '',
        'Chapter 9: Same-Side Rotators'
    ]
))

# Neck Rotators - Opposite Side
deck.add_note(genanki.Note(
    model=basic_model,
    fields=[
        'Which neck muscles rotate to the OPPOSITE side?',
        '<ul><li>Sternocleidomastoid</li><li>Transversospinalis group</li></ul>',
        'Chapter 9: Opposite-Side Rotators'
    ]
))

deck.add_note(genanki.Note(
    model=cloze_model,
    fields=[
        'Opposite-side neck rotators include {{c1::sternocleidomastoid}} and the {{c2::transversospinalis}} group.',
        '',
        'Chapter 9: Opposite-Side Rotators'
    ]
))

# Comparison card for neck rotators
deck.add_note(genanki.Note(
    model=comparison_model,
    fields=[
        'Same-side vs. Opposite-side neck rotators',
        '<strong>Same side (Ipsilateral):</strong><ul><li>Splenii / Splenius Group</li><li>Obliquus capitis inferior</li><li>Rectus capitis posterior major</li></ul><strong>Opposite side (Contralateral):</strong><ul><li>Sternocleidomastoid</li><li>Transversospinalis group</li></ul><div class="emphasis">Key: SCM goes opposite, Splenii go same!</div>',
        'Chapter 9: Neck Rotators Comparison'
    ]
))

# Trunk Flexors
deck.add_note(genanki.Note(
    model=basic_model,
    fields=[
        'What are the primary trunk flexors?',
        '<ul><li>Rectus abdominis</li><li>External oblique (bilateral)</li><li>Internal oblique (bilateral)</li></ul>',
        'Chapter 9: Trunk Flexors'
    ]
))

deck.add_note(genanki.Note(
    model=basic_reverse_model,
    fields=[
        'Rectus abdominis',
        'Actions:<br>- Trunk flexion<br>- Compression of abdomen',
        'Chapter 9: Trunk'
    ]
))

deck.add_note(genanki.Note(
    model=cloze_model,
    fields=[
        'The rectus abdominis performs {{c1::trunk flexion}} and {{c2::compression of abdomen}}.',
        '',
        'Chapter 9: Rectus Abdominis'
    ]
))

# Trunk Extensors
deck.add_note(genanki.Note(
    model=basic_model,
    fields=[
        'What are the primary trunk extensors?',
        '<ul><li>Erector spinae</li><li>Transversospinalis</li></ul>',
        'Chapter 9: Trunk Extensors'
    ]
))

deck.add_note(genanki.Note(
    model=cloze_model,
    fields=[
        'The two major trunk extensor groups are {{c1::erector spinae}} and {{c2::transversospinalis}}.',
        '',
        'Chapter 9: Trunk Extensors'
    ]
))

# Erector Spinae Details
deck.add_note(genanki.Note(
    model=basic_reverse_model,
    fields=[
        'Erector Spinae Group',
        'Muscles: Iliocostalis, Longissimus, Spinalis<br>Bilateral: Trunk/spine extension<br>Unilateral: Lateral flexion<br>Location: Superficial on posterior trunk',
        'Chapter 9: Erector Spinae'
    ]
))

deck.add_note(genanki.Note(
    model=cloze_model,
    fields=[
        'The erector spinae group consists of {{c1::iliocostalis}}, {{c2::longissimus}}, and {{c3::spinalis}}.',
        'Located superficially on the posterior trunk',
        'Chapter 9: Erector Spinae'
    ]
))

deck.add_note(genanki.Note(
    model=cloze_model,
    fields=[
        'When contracting bilaterally, the erector spinae produces {{c1::trunk/spine extension}}. When contracting unilaterally, it produces {{c2::lateral flexion}}.',
        '',
        'Chapter 9: Erector Spinae Actions'
    ]
))

# Transversospinalis Details
deck.add_note(genanki.Note(
    model=basic_reverse_model,
    fields=[
        'Transversospinalis Group',
        'Muscles: Semispinalis, Multifidus, Rotatores<br>Bilateral: Extension<br>Unilateral: Rotation to opposite side<br>Location: Deep to erector spinae',
        'Chapter 9: Transversospinalis'
    ]
))

deck.add_note(genanki.Note(
    model=cloze_model,
    fields=[
        'The transversospinalis group consists of {{c1::semispinalis}}, {{c2::multifidus}}, and {{c3::rotatores}}.',
        'Located deep to erector spinae',
        'Chapter 9: Transversospinalis'
    ]
))

deck.add_note(genanki.Note(
    model=cloze_model,
    fields=[
        'The transversospinalis group is located {{c1::deep}} to the erector spinae.',
        '',
        'Chapter 9: Muscle Layers'
    ]
))

deck.add_note(genanki.Note(
    model=cloze_model,
    fields=[
        'When the transversospinalis contracts bilaterally, it produces {{c1::extension}}. When it contracts unilaterally, it produces rotation to the {{c2::opposite side}}.',
        '',
        'Chapter 9: Transversospinalis Actions'
    ]
))

# Comparison: Erector Spinae vs Transversospinalis
deck.add_note(genanki.Note(
    model=comparison_model,
    fields=[
        'Erector Spinae vs. Transversospinalis',
        '<strong>Erector Spinae:</strong><ul><li>Location: Superficial</li><li>Muscles: Iliocostalis, Longissimus, Spinalis</li><li>Unilateral: Lateral flexion</li></ul><strong>Transversospinalis:</strong><ul><li>Location: Deep to ES</li><li>Muscles: Semispinalis, Multifidus, Rotatores</li><li>Unilateral: Rotation to opposite side</li></ul><div class="emphasis">Both: Bilateral extension</div>',
        'Chapter 9: Back Muscle Layers'
    ]
))

# Trunk Lateral Flexors
deck.add_note(genanki.Note(
    model=basic_model,
    fields=[
        'What muscles perform lateral flexion of the trunk?',
        '<ul><li>Quadratus lumborum</li><li>Erector spinae</li><li>Internal oblique (unilateral)</li><li>External oblique (unilateral)</li></ul>',
        'Chapter 9: Trunk Lateral Flexors'
    ]
))

deck.add_note(genanki.Note(
    model=cloze_model,
    fields=[
        'Trunk lateral flexion is performed by {{c1::quadratus lumborum}}, {{c2::erector spinae}}, and unilateral contraction of the {{c3::internal oblique}} and {{c4::external oblique}}.',
        '',
        'Chapter 9: Trunk Lateral Flexors'
    ]
))

# Trunk Rotators - Internal vs External Obliques
deck.add_note(genanki.Note(
    model=basic_reverse_model,
    fields=[
        'Internal Oblique (Unilateral)',
        'Actions:<br>- Rotation to SAME side<br>- Lateral flexion to same side<br><br>Bilateral: Trunk flexion, abdominal compression',
        'Chapter 9: Internal Oblique'
    ]
))

deck.add_note(genanki.Note(
    model=basic_reverse_model,
    fields=[
        'External Oblique (Unilateral)',
        'Actions:<br>- Rotation to OPPOSITE side<br>- Lateral flexion to same side<br><br>Bilateral: Trunk flexion, abdominal compression',
        'Chapter 9: External Oblique'
    ]
))

deck.add_note(genanki.Note(
    model=cloze_model,
    fields=[
        'The {{c1::internal oblique}} rotates to the {{c2::same}} side, while the {{c3::external oblique}} rotates to the {{c4::opposite}} side.',
        '',
        'Chapter 9: Oblique Rotations'
    ]
))

deck.add_note(genanki.Note(
    model=comparison_model,
    fields=[
        'Internal Oblique vs. External Oblique rotation patterns',
        '<strong>Internal Oblique (Unilateral):</strong><ul><li>Rotation to SAME side</li><li>Lateral flexion to same side</li></ul><strong>External Oblique (Unilateral):</strong><ul><li>Rotation to OPPOSITE side</li><li>Lateral flexion to same side</li></ul><strong>Both (Bilateral):</strong><ul><li>Trunk flexion</li><li>Abdominal compression</li></ul><div class="emphasis">Remember: Internal = Ipsilateral, External = Contralateral</div>',
        'Chapter 9: Obliques Comparison'
    ]
))

deck.add_note(genanki.Note(
    model=cloze_model,
    fields=[
        'Both internal and external obliques produce {{c1::lateral flexion to the same side}} when contracting unilaterally.',
        '',
        'Chapter 9: Obliques Lateral Flexion'
    ]
))

# Trunk Rotators - Same Side
deck.add_note(genanki.Note(
    model=basic_model,
    fields=[
        'Which trunk muscles rotate to the SAME side?',
        '<ul><li>Internal oblique (unilateral)</li><li>Splenius cervicis</li></ul>',
        'Chapter 9: Same-Side Trunk Rotators'
    ]
))

# Trunk Rotators - Opposite Side
deck.add_note(genanki.Note(
    model=basic_model,
    fields=[
        'Which trunk muscles rotate to the OPPOSITE side?',
        '<ul><li>External oblique (unilateral)</li><li>Transversospinalis group (Semispinalis, Multifidus, Rotatores)</li></ul>',
        'Chapter 9: Opposite-Side Trunk Rotators'
    ]
))

# Splenius Cervicis
deck.add_note(genanki.Note(
    model=basic_reverse_model,
    fields=[
        'Splenius Cervicis',
        'Actions:<br>- Extension<br>- Rotation to same side',
        'Chapter 9: Splenius Cervicis'
    ]
))

# Abdominal Compression
deck.add_note(genanki.Note(
    model=basic_model,
    fields=[
        'Which muscles compress the abdomen?',
        '<ul><li>Rectus abdominis</li><li>External oblique</li><li>Internal oblique</li><li>Transversus abdominis</li></ul>',
        'Chapter 9: Abdominal Compression'
    ]
))

deck.add_note(genanki.Note(
    model=cloze_model,
    fields=[
        'The four muscles that compress the abdomen are {{c1::rectus abdominis}}, {{c2::external oblique}}, {{c3::internal oblique}}, and {{c4::transversus abdominis}}.',
        '',
        'Chapter 9: Abdominal Compression'
    ]
))

# Respiration - Inhalation
deck.add_note(genanki.Note(
    model=basic_model,
    fields=[
        'Which muscles are primary for inhalation?',
        '<ul><li>Diaphragm</li><li>External intercostals (elevate ribs)</li></ul>',
        'Chapter 9: Inhalation Muscles'
    ]
))

deck.add_note(genanki.Note(
    model=cloze_model,
    fields=[
        'The primary inhalation muscles are the {{c1::diaphragm}} and {{c2::external intercostals}}, which {{c3::elevate}} the ribs.',
        '',
        'Chapter 9: Inhalation'
    ]
))

# Respiration - Exhalation
deck.add_note(genanki.Note(
    model=basic_model,
    fields=[
        'Which muscles are active during forced exhalation?',
        'Internal intercostals (depress ribs)',
        'Chapter 9: Exhalation Muscles'
    ]
))

deck.add_note(genanki.Note(
    model=cloze_model,
    fields=[
        'The {{c1::internal intercostals}} assist with forced exhalation by {{c2::depressing}} the ribs.',
        '',
        'Chapter 9: Exhalation'
    ]
))

# Comparison: Intercostals
deck.add_note(genanki.Note(
    model=comparison_model,
    fields=[
        'External vs. Internal Intercostals',
        '<strong>External Intercostals:</strong><ul><li>Elevate ribs</li><li>Function: Inhalation</li></ul><strong>Internal Intercostals:</strong><ul><li>Depress ribs</li><li>Function: Forced exhalation</li></ul>',
        'Chapter 9: Respiration'
    ]
))

# ============================================================================
# CHAPTER 10: PELVIS
# ============================================================================

# Anterior Pelvic Tilt - Associated Movements
deck.add_note(genanki.Note(
    model=basic_model,
    fields=[
        'What movements are associated with anterior pelvic tilt?',
        '<ul><li>Lumbar extension (increased lordosis)</li><li>Hip flexion</li></ul>',
        'Chapter 10: Anterior Pelvic Tilt'
    ]
))

deck.add_note(genanki.Note(
    model=cloze_model,
    fields=[
        'Anterior pelvic tilt is associated with {{c1::lumbar extension}} (increased lordosis) and {{c2::hip flexion}}.',
        '',
        'Chapter 10: Anterior Pelvic Tilt'
    ]
))

# Anterior Pelvic Tilt - Force Couple
deck.add_note(genanki.Note(
    model=clinical_model,
    fields=[
        'What is the force couple that produces anterior pelvic tilt?',
        '<strong>Trunk extensors</strong> (pull upward on posterior pelvis):<ul><li>Erector spinae</li><li>Transversospinalis</li></ul><strong>Hip flexors</strong> (pull downward on anterior pelvis):<ul><li>Iliopsoas</li><li>Rectus femoris</li><li>Pectineus</li></ul>',
        'Force couples are pairs/groups of muscles that work together to produce a movement',
        'Chapter 10: Anterior Pelvic Tilt Force Couple'
    ]
))

deck.add_note(genanki.Note(
    model=cloze_model,
    fields=[
        'The anterior pelvic tilt force couple consists of {{c1::trunk extensors}} pulling upward on the posterior pelvis and {{c2::hip flexors}} pulling downward on the anterior pelvis.',
        '',
        'Chapter 10: APT Force Couple'
    ]
))

deck.add_note(genanki.Note(
    model=cloze_model,
    fields=[
        'In the anterior pelvic tilt force couple, the trunk extensors include {{c1::erector spinae}} and {{c2::transversospinalis}}, while the hip flexors include {{c3::iliopsoas}}, {{c4::rectus femoris}}, and {{c5::pectineus}}.',
        '',
        'Chapter 10: APT Force Couple Muscles'
    ]
))

# Posterior Pelvic Tilt - Associated Movements
deck.add_note(genanki.Note(
    model=basic_model,
    fields=[
        'What movements are associated with posterior pelvic tilt?',
        '<ul><li>Lumbar flexion (decreased lordosis)</li><li>Hip extension</li></ul>',
        'Chapter 10: Posterior Pelvic Tilt'
    ]
))

deck.add_note(genanki.Note(
    model=cloze_model,
    fields=[
        'Posterior pelvic tilt is associated with {{c1::lumbar flexion}} (decreased lordosis) and {{c2::hip extension}}.',
        '',
        'Chapter 10: Posterior Pelvic Tilt'
    ]
))

# Posterior Pelvic Tilt - Force Couple
deck.add_note(genanki.Note(
    model=clinical_model,
    fields=[
        'What is the force couple that produces posterior pelvic tilt?',
        '<strong>Trunk flexors</strong> (pull upward on anterior pelvis):<ul><li>Rectus abdominis</li><li>External oblique</li><li>Internal oblique</li></ul><strong>Hip extensors</strong> (pull downward on posterior pelvis):<ul><li>Gluteus maximus</li><li>Hamstrings: Biceps femoris (long head), Semitendinosus, Semimembranosus</li></ul>',
        'Force couples are pairs/groups of muscles that work together to produce a movement',
        'Chapter 10: Posterior Pelvic Tilt Force Couple'
    ]
))

deck.add_note(genanki.Note(
    model=cloze_model,
    fields=[
        'The posterior pelvic tilt force couple consists of {{c1::trunk flexors}} pulling upward on the anterior pelvis and {{c2::hip extensors}} pulling downward on the posterior pelvis.',
        '',
        'Chapter 10: PPT Force Couple'
    ]
))

deck.add_note(genanki.Note(
    model=cloze_model,
    fields=[
        'In the posterior pelvic tilt force couple, the trunk flexors include {{c1::rectus abdominis}}, {{c2::external oblique}}, and {{c3::internal oblique}}.',
        '',
        'Chapter 10: PPT Trunk Flexors'
    ]
))

deck.add_note(genanki.Note(
    model=cloze_model,
    fields=[
        'In the posterior pelvic tilt force couple, the hip extensors include {{c1::gluteus maximus}} and the hamstrings ({{c2::biceps femoris}} long head, {{c3::semitendinosus}}, {{c4::semimembranosus}}).',
        '',
        'Chapter 10: PPT Hip Extensors'
    ]
))

# Comparison: Anterior vs Posterior Pelvic Tilt
deck.add_note(genanki.Note(
    model=comparison_model,
    fields=[
        'Anterior vs. Posterior Pelvic Tilt',
        '<strong>Anterior Pelvic Tilt:</strong><ul><li>Lumbar extension (↑ lordosis)</li><li>Hip flexion</li><li>Force couple: Trunk extensors + Hip flexors</li></ul><strong>Posterior Pelvic Tilt:</strong><ul><li>Lumbar flexion (↓ lordosis)</li><li>Hip extension</li><li>Force couple: Trunk flexors + Hip extensors</li></ul>',
        'Chapter 10: Pelvic Tilts'
    ]
))

# Lateral Pelvic Tilt - Associated Movements
deck.add_note(genanki.Note(
    model=basic_model,
    fields=[
        'What movements are associated with lateral pelvic tilt during single-leg stance?',
        '<ul><li>Lateral bending to supported/stance side</li><li>Hip adduction on weight-bearing side</li><li>Hip abduction on non-weight-bearing side</li></ul>',
        'Chapter 10: Lateral Pelvic Tilt'
    ]
))

deck.add_note(genanki.Note(
    model=cloze_model,
    fields=[
        'During single-leg stance, lateral pelvic tilt involves {{c1::lateral bending}} to the supported side, {{c2::hip adduction}} on the weight-bearing side, and {{c3::hip abduction}} on the non-weight-bearing side.',
        '',
        'Chapter 10: Lateral Pelvic Tilt'
    ]
))

# Lateral Pelvic Tilt - Force Couple
deck.add_note(genanki.Note(
    model=clinical_model,
    fields=[
        'What is the force couple that maintains level pelvis during single-leg stance?',
        '<strong>Lateral trunk flexors on stance side</strong> (pull upward on pelvis):<ul><li>Erector spinae</li><li>Quadratus lumborum</li></ul><strong>Hip abductors on stance side</strong> (pull downward on pelvis):<ul><li>Gluteus medius</li><li>Gluteus minimus</li></ul>',
        'During gait, when one leg leaves the ground, gravity causes the unsupported side to drop. This force couple prevents that drop.',
        'Chapter 10: Lateral Pelvic Tilt Force Couple'
    ]
))

deck.add_note(genanki.Note(
    model=cloze_model,
    fields=[
        'The lateral pelvic tilt force couple consists of {{c1::lateral trunk flexors}} on the stance side pulling upward and {{c2::hip abductors}} on the stance side pulling downward.',
        '',
        'Chapter 10: Lateral Tilt Force Couple'
    ]
))

deck.add_note(genanki.Note(
    model=cloze_model,
    fields=[
        'During single-leg stance, the lateral trunk flexors include {{c1::erector spinae}} and {{c2::quadratus lumborum}}, while the hip abductors include {{c3::gluteus medius}} and {{c4::gluteus minimus}}.',
        '',
        'Chapter 10: Lateral Tilt Muscles'
    ]
))

# Clinical Note on Gait
deck.add_note(genanki.Note(
    model=clinical_model,
    fields=[
        'What happens to the pelvis during gait when one leg leaves the ground?',
        'Gravity causes the unsupported side of the pelvis to drop (lateral tilt). The force couple on the stance leg (lateral trunk flexors + hip abductors) works to maintain the pelvis level.',
        'This is critical for normal gait mechanics',
        'Chapter 10: Gait Mechanics'
    ]
))

# Pelvic Rotation Forward
deck.add_note(genanki.Note(
    model=basic_model,
    fields=[
        'What movements are associated with forward pelvic rotation?',
        '<ul><li>Vertebral rotation to opposite side</li><li>Hip medial rotation on weight-bearing side</li></ul>',
        'Chapter 10: Forward Pelvic Rotation'
    ]
))

deck.add_note(genanki.Note(
    model=cloze_model,
    fields=[
        'Forward pelvic rotation is associated with {{c1::vertebral rotation}} to the {{c2::opposite}} side and {{c3::hip medial rotation}} on the weight-bearing side.',
        '',
        'Chapter 10: Forward Pelvic Rotation'
    ]
))

# Pelvic Rotation Backward
deck.add_note(genanki.Note(
    model=basic_model,
    fields=[
        'What movements are associated with backward pelvic rotation?',
        '<ul><li>Vertebral rotation to opposite side</li><li>Hip lateral rotation on weight-bearing side</li></ul>',
        'Chapter 10: Backward Pelvic Rotation'
    ]
))

deck.add_note(genanki.Note(
    model=cloze_model,
    fields=[
        'Backward pelvic rotation is associated with {{c1::vertebral rotation}} to the {{c2::opposite}} side and {{c3::hip lateral rotation}} on the weight-bearing side.',
        '',
        'Chapter 10: Backward Pelvic Rotation'
    ]
))

# Chronic Anterior Pelvic Tilt Posture
deck.add_note(genanki.Note(
    model=clinical_model,
    fields=[
        'In chronic anterior pelvic tilt posture, which muscles are adaptively shortened (tight)?',
        '<ul><li>Trunk extensors</li><li>Hip flexors</li></ul>',
        'This creates a muscle imbalance pattern',
        'Chapter 10: APT Posture - Tight Muscles'
    ]
))

deck.add_note(genanki.Note(
    model=clinical_model,
    fields=[
        'In chronic anterior pelvic tilt posture, which muscles are adaptively lengthened (weak)?',
        '<ul><li>Trunk flexors</li><li>Hip extensors</li></ul>',
        'This creates a muscle imbalance pattern',
        'Chapter 10: APT Posture - Weak Muscles'
    ]
))

deck.add_note(genanki.Note(
    model=cloze_model,
    fields=[
        'In chronic anterior pelvic tilt posture, {{c1::trunk extensors}} and {{c2::hip flexors}} are adaptively shortened (tight), while {{c3::trunk flexors}} and {{c4::hip extensors}} are adaptively lengthened (weak).',
        '',
        'Chapter 10: APT Posture Pattern'
    ]
))

# Chronic Posterior Pelvic Tilt Posture
deck.add_note(genanki.Note(
    model=clinical_model,
    fields=[
        'In chronic posterior pelvic tilt posture, which muscles are adaptively shortened (tight)?',
        '<ul><li>Trunk flexors</li><li>Hip extensors</li></ul>',
        'This creates a muscle imbalance pattern',
        'Chapter 10: PPT Posture - Tight Muscles'
    ]
))

deck.add_note(genanki.Note(
    model=clinical_model,
    fields=[
        'In chronic posterior pelvic tilt posture, which muscles are adaptively lengthened (weak)?',
        '<ul><li>Trunk extensors</li><li>Hip flexors</li></ul>',
        'This creates a muscle imbalance pattern',
        'Chapter 10: PPT Posture - Weak Muscles'
    ]
))

deck.add_note(genanki.Note(
    model=cloze_model,
    fields=[
        'In chronic posterior pelvic tilt posture, {{c1::trunk flexors}} and {{c2::hip extensors}} are adaptively shortened (tight), while {{c3::trunk extensors}} and {{c4::hip flexors}} are adaptively lengthened (weak).',
        '',
        'Chapter 10: PPT Posture Pattern'
    ]
))

# Comparison: APT vs PPT Posture
deck.add_note(genanki.Note(
    model=comparison_model,
    fields=[
        'Chronic Anterior vs. Posterior Pelvic Tilt Posture muscle imbalances',
        '<strong>Anterior Pelvic Tilt Posture:</strong><ul><li>Tight: Trunk extensors, Hip flexors</li><li>Weak: Trunk flexors, Hip extensors</li></ul><strong>Posterior Pelvic Tilt Posture:</strong><ul><li>Tight: Trunk flexors, Hip extensors</li><li>Weak: Trunk extensors, Hip flexors</li></ul><div class="emphasis">Notice the pattern reversal!</div>',
        'Chapter 10: Postural Imbalances'
    ]
))

# ============================================================================
# CHAPTER 12: SHOULDER GIRDLE (SCAPULOTHORACIC)
# ============================================================================

# Scapular Retractors
deck.add_note(genanki.Note(
    model=basic_model,
    fields=[
        'What muscles retract (adduct) the scapula?',
        '<ul><li>Trapezius (all three portions: upper, middle, lower)</li><li>Rhomboids (major and minor)</li></ul>',
        'Chapter 12: Scapular Retractors'
    ]
))

deck.add_note(genanki.Note(
    model=cloze_model,
    fields=[
        'Scapular retraction is performed by all three portions of the {{c1::trapezius}} and the {{c2::rhomboids}}.',
        '',
        'Chapter 12: Scapular Retractors'
    ]
))

# Scapular Protractors
deck.add_note(genanki.Note(
    model=basic_model,
    fields=[
        'What muscles protract (abduct) the scapula?',
        '<ul><li>Serratus anterior</li><li>Pectoralis minor</li></ul>',
        'Chapter 12: Scapular Protractors'
    ]
))

deck.add_note(genanki.Note(
    model=cloze_model,
    fields=[
        'Scapular protraction is performed by {{c1::serratus anterior}} and {{c2::pectoralis minor}}.',
        '',
        'Chapter 12: Scapular Protractors'
    ]
))

# Scapular Elevators
deck.add_note(genanki.Note(
    model=basic_model,
    fields=[
        'What muscles elevate the scapula?',
        '<ul><li>Upper trapezius</li><li>Middle trapezius</li><li>Levator scapulae</li><li>Rhomboids</li></ul>',
        'Chapter 12: Scapular Elevators'
    ]
))

deck.add_note(genanki.Note(
    model=cloze_model,
    fields=[
        'Scapular elevation is performed by {{c1::upper trapezius}}, {{c2::middle trapezius}}, {{c3::levator scapulae}}, and {{c4::rhomboids}}.',
        '',
        'Chapter 12: Scapular Elevators'
    ]
))

# Scapular Depressors
deck.add_note(genanki.Note(
    model=basic_model,
    fields=[
        'What muscles depress the scapula?',
        '<ul><li>Lower trapezius</li><li>Pectoralis minor</li></ul>',
        'Chapter 12: Scapular Depressors'
    ]
))

deck.add_note(genanki.Note(
    model=cloze_model,
    fields=[
        'Scapular depression is performed by {{c1::lower trapezius}} and {{c2::pectoralis minor}}.',
        '',
        'Chapter 12: Scapular Depressors'
    ]
))

# Scapular Upward Rotators
deck.add_note(genanki.Note(
    model=basic_model,
    fields=[
        'What muscles produce upward rotation of the scapula?',
        '<ul><li>Trapezius (all three portions)</li><li>Serratus anterior (lower fibers)</li></ul>',
        'Chapter 12: Scapular Upward Rotators'
    ]
))

deck.add_note(genanki.Note(
    model=cloze_model,
    fields=[
        'Scapular upward rotation is performed by all three portions of the {{c1::trapezius}} and the {{c2::serratus anterior}} (lower fibers).',
        '',
        'Chapter 12: Scapular Upward Rotators'
    ]
))

# Clinical: SLUT Force Couple
deck.add_note(genanki.Note(
    model=clinical_model,
    fields=[
        'What is the "SLUT" force couple for scapular upward rotation?',
        '<ul><li><strong>S</strong>erratus anterior</li><li><strong>L</strong>ower trapezius</li><li><strong>U</strong>pper trapezius</li><li><strong>T</strong>rapezius (all portions)</li></ul>',
        'Mnemonic: SLUT = Serratus anterior + Lower/Upper Trapezius',
        'Chapter 12: Scapular Force Couples'
    ]
))

deck.add_note(genanki.Note(
    model=cloze_model,
    fields=[
        'The SLUT force couple for scapular upward rotation consists of {{c1::Serratus anterior}}, {{c2::Lower trapezius}}, and {{c3::Upper Trapezius}}.',
        '',
        'Chapter 12: SLUT Force Couple'
    ]
))

# Scapular Downward Rotators
deck.add_note(genanki.Note(
    model=basic_model,
    fields=[
        'What muscles produce downward rotation of the scapula?',
        '<ul><li>Rhomboids</li><li>Levator scapulae</li><li>Pectoralis minor</li></ul>',
        'Chapter 12: Scapular Downward Rotators'
    ]
))

deck.add_note(genanki.Note(
    model=cloze_model,
    fields=[
        'Scapular downward rotation is performed by {{c1::rhomboids}}, {{c2::levator scapulae}}, and {{c3::pectoralis minor}}.',
        '',
        'Chapter 12: Scapular Downward Rotators'
    ]
))

# Clinical: PRL Force Couple
deck.add_note(genanki.Note(
    model=clinical_model,
    fields=[
        'What is the "PRL" force couple for scapular downward rotation?',
        '<ul><li><strong>P</strong>ectoralis minor</li><li><strong>R</strong>homboids</li><li><strong>L</strong>evator scapulae</li></ul>',
        'Mnemonic: PRL = Pectoralis minor + Rhomboids + Levator scapulae',
        'Chapter 12: Scapular Force Couples'
    ]
))

deck.add_note(genanki.Note(
    model=cloze_model,
    fields=[
        'The PRL force couple for scapular downward rotation consists of {{c1::Pectoralis minor}}, {{c2::Rhomboids}}, and {{c3::Levator scapulae}}.',
        '',
        'Chapter 12: PRL Force Couple'
    ]
))

# Scapular Tilt
deck.add_note(genanki.Note(
    model=basic_model,
    fields=[
        'Which muscle produces anterior tilt of the scapula?',
        'Pectoralis minor',
        'Chapter 12: Scapular Tilt'
    ]
))

deck.add_note(genanki.Note(
    model=cloze_model,
    fields=[
        'The {{c1::pectoralis minor}} produces anterior tilt of the scapula.',
        '',
        'Chapter 12: Scapular Tilt'
    ]
))

# Trapezius - Multi-action
deck.add_note(genanki.Note(
    model=basic_reverse_model,
    fields=[
        'Trapezius (all portions)',
        '<strong>Upper:</strong> Scapular elevation, upward rotation, retraction<br><strong>Middle:</strong> Scapular retraction, upward rotation<br><strong>Lower:</strong> Scapular depression, upward rotation, retraction',
        'Chapter 12: Trapezius Multi-Actions'
    ]
))

deck.add_note(genanki.Note(
    model=cloze_model,
    fields=[
        'All three portions of the trapezius perform {{c1::scapular retraction}} and {{c2::upward rotation}}.',
        '',
        'Chapter 12: Trapezius Common Actions'
    ]
))

# Comparison: Upward vs Downward Rotation
deck.add_note(genanki.Note(
    model=comparison_model,
    fields=[
        'Scapular Upward vs. Downward Rotation',
        '<strong>Upward Rotation:</strong><ul><li>Trapezius (all portions)</li><li>Serratus anterior</li><li>Mnemonic: SLUT</li></ul><strong>Downward Rotation:</strong><ul><li>Rhomboids</li><li>Levator scapulae</li><li>Pectoralis minor</li><li>Mnemonic: PRL</li></ul>',
        'Chapter 12: Scapular Rotation'
    ]
))

# Pectoralis Minor - Multi-action
deck.add_note(genanki.Note(
    model=basic_reverse_model,
    fields=[
        'Pectoralis Minor',
        'Actions:<br><ul><li>Scapular protraction</li><li>Scapular depression</li><li>Scapular downward rotation</li><li>Scapular anterior tilt</li></ul>',
        'Chapter 12: Pectoralis Minor'
    ]
))

deck.add_note(genanki.Note(
    model=cloze_model,
    fields=[
        'Pectoralis minor performs scapular {{c1::protraction}}, {{c2::depression}}, {{c3::downward rotation}}, and {{c4::anterior tilt}}.',
        '',
        'Chapter 12: Pectoralis Minor Actions'
    ]
))

# ============================================================================
# CHAPTER 13: SHOULDER JOINT (GLENOHUMERAL)
# ============================================================================

# Shoulder Flexors
deck.add_note(genanki.Note(
    model=basic_model,
    fields=[
        'What are the primary shoulder flexors?',
        '<ul><li>Anterior deltoid</li><li>Pectoralis major (clavicular portion) - to approximately 60 degrees</li></ul>',
        'Chapter 13: Shoulder Flexors'
    ]
))

deck.add_note(genanki.Note(
    model=cloze_model,
    fields=[
        'The primary shoulder flexors are {{c1::anterior deltoid}} and {{c2::pectoralis major}} (clavicular portion).',
        '',
        'Chapter 13: Shoulder Flexors'
    ]
))

deck.add_note(genanki.Note(
    model=cloze_model,
    fields=[
        'Pectoralis major (clavicular portion) performs shoulder flexion only to approximately {{c1::60}} degrees.',
        '',
        'Chapter 13: Pec Major ROM'
    ]
))

# Shoulder Extensors
deck.add_note(genanki.Note(
    model=basic_model,
    fields=[
        'What are the primary shoulder extensors?',
        '<ul><li>Posterior deltoid</li><li>Latissimus dorsi</li><li>Teres major</li><li>Pectoralis major (sternal portion) - to approximately 120 degrees</li></ul>',
        'Chapter 13: Shoulder Extensors'
    ]
))

deck.add_note(genanki.Note(
    model=cloze_model,
    fields=[
        'The shoulder extensors include {{c1::posterior deltoid}}, {{c2::latissimus dorsi}}, {{c3::teres major}}, and {{c4::pectoralis major}} (sternal portion).',
        '',
        'Chapter 13: Shoulder Extensors'
    ]
))

deck.add_note(genanki.Note(
    model=cloze_model,
    fields=[
        'Pectoralis major (sternal portion) performs shoulder extension only to approximately {{c1::120}} degrees.',
        '',
        'Chapter 13: Pec Major Sternal ROM'
    ]
))

# Shoulder Abductors
deck.add_note(genanki.Note(
    model=basic_model,
    fields=[
        'What are the primary shoulder abductors?',
        '<ul><li>Deltoid (middle/acromial fibers - primary)</li><li>Supraspinatus (initiates and assists abduction)</li></ul>',
        'Chapter 13: Shoulder Abductors'
    ]
))

deck.add_note(genanki.Note(
    model=cloze_model,
    fields=[
        'The primary shoulder abductor is the {{c1::deltoid}} (middle/acromial fibers), while {{c2::supraspinatus}} initiates and assists abduction.',
        '',
        'Chapter 13: Shoulder Abductors'
    ]
))

deck.add_note(genanki.Note(
    model=cloze_model,
    fields=[
        'Supraspinatus initiates abduction during the first {{c1::15-30}} degrees, then the {{c2::deltoid}} takes over.',
        '',
        'Chapter 13: Abduction Initiation'
    ]
))

# Shoulder Adductors
deck.add_note(genanki.Note(
    model=basic_model,
    fields=[
        'What are the primary shoulder adductors?',
        '<ul><li>Pectoralis major</li><li>Teres major</li><li>Latissimus dorsi</li></ul>',
        'Chapter 13: Shoulder Adductors'
    ]
))

deck.add_note(genanki.Note(
    model=cloze_model,
    fields=[
        'The shoulder adductors are {{c1::pectoralis major}}, {{c2::teres major}}, and {{c3::latissimus dorsi}}.',
        '',
        'Chapter 13: Shoulder Adductors'
    ]
))

# Shoulder Horizontal Abductors
deck.add_note(genanki.Note(
    model=basic_model,
    fields=[
        'What muscles perform shoulder horizontal abduction?',
        '<ul><li>Posterior deltoid</li><li>Infraspinatus</li><li>Teres minor</li></ul>',
        'Chapter 13: Shoulder Horizontal Abductors'
    ]
))

deck.add_note(genanki.Note(
    model=cloze_model,
    fields=[
        'Shoulder horizontal abduction is performed by {{c1::posterior deltoid}}, {{c2::infraspinatus}}, and {{c3::teres minor}}.',
        '',
        'Chapter 13: Horizontal Abductors'
    ]
))

# Shoulder Horizontal Adductors
deck.add_note(genanki.Note(
    model=basic_model,
    fields=[
        'What muscles perform shoulder horizontal adduction?',
        '<ul><li>Pectoralis major</li><li>Anterior deltoid</li></ul>',
        'Chapter 13: Shoulder Horizontal Adductors'
    ]
))

deck.add_note(genanki.Note(
    model=cloze_model,
    fields=[
        'Shoulder horizontal adduction is performed by {{c1::pectoralis major}} and {{c2::anterior deltoid}}.',
        '',
        'Chapter 13: Horizontal Adductors'
    ]
))

# Shoulder Lateral Rotators
deck.add_note(genanki.Note(
    model=basic_model,
    fields=[
        'What muscles perform shoulder lateral (external) rotation?',
        '<ul><li>Infraspinatus</li><li>Teres minor</li><li>Posterior deltoid</li></ul>',
        'Chapter 13: Shoulder Lateral Rotators'
    ]
))

deck.add_note(genanki.Note(
    model=cloze_model,
    fields=[
        'Shoulder lateral rotation is performed by {{c1::infraspinatus}}, {{c2::teres minor}}, and {{c3::posterior deltoid}}.',
        '',
        'Chapter 13: Lateral Rotators'
    ]
))

# Shoulder Medial Rotators
deck.add_note(genanki.Note(
    model=basic_model,
    fields=[
        'What muscles perform shoulder medial (internal) rotation?',
        '<ul><li>Latissimus dorsi</li><li>Teres major</li><li>Subscapularis</li><li>Pectoralis major</li><li>Anterior deltoid</li></ul>',
        'Chapter 13: Shoulder Medial Rotators'
    ]
))

deck.add_note(genanki.Note(
    model=cloze_model,
    fields=[
        'Shoulder medial rotation is performed by {{c1::latissimus dorsi}}, {{c2::teres major}}, {{c3::subscapularis}}, {{c4::pectoralis major}}, and {{c5::anterior deltoid}}.',
        '',
        'Chapter 13: Medial Rotators'
    ]
))

# Deltoid - Three Portions
deck.add_note(genanki.Note(
    model=basic_reverse_model,
    fields=[
        'Deltoid (3 distinct portions)',
        '<strong>Anterior:</strong> Flexion, horizontal adduction, medial rotation<br><strong>Middle/Acromial:</strong> Abduction (primary)<br><strong>Posterior:</strong> Extension, horizontal abduction, lateral rotation',
        'Chapter 13: Deltoid Multi-Actions'
    ]
))

deck.add_note(genanki.Note(
    model=cloze_model,
    fields=[
        'The anterior deltoid performs {{c1::flexion}}, {{c2::horizontal adduction}}, and {{c3::medial rotation}}.',
        '',
        'Chapter 13: Anterior Deltoid'
    ]
))

deck.add_note(genanki.Note(
    model=cloze_model,
    fields=[
        'The middle/acromial deltoid is the primary {{c1::abductor}} of the shoulder.',
        '',
        'Chapter 13: Middle Deltoid'
    ]
))

deck.add_note(genanki.Note(
    model=cloze_model,
    fields=[
        'The posterior deltoid performs {{c1::extension}}, {{c2::horizontal abduction}}, and {{c3::lateral rotation}}.',
        '',
        'Chapter 13: Posterior Deltoid'
    ]
))

# Comparison: Anterior vs Posterior Deltoid
deck.add_note(genanki.Note(
    model=comparison_model,
    fields=[
        'Anterior vs. Posterior Deltoid',
        '<strong>Anterior Deltoid:</strong><ul><li>Flexion</li><li>Horizontal adduction</li><li>Medial rotation</li></ul><strong>Posterior Deltoid:</strong><ul><li>Extension</li><li>Horizontal abduction</li><li>Lateral rotation</li></ul><strong>Middle Deltoid:</strong><ul><li>Abduction (primary)</li></ul>',
        'Chapter 13: Deltoid Comparison'
    ]
))

# Pectoralis Major - Two Portions
deck.add_note(genanki.Note(
    model=basic_reverse_model,
    fields=[
        'Pectoralis Major (2 portions)',
        '<strong>Clavicular:</strong> Flexion (to ~60°), horizontal adduction, medial rotation<br><strong>Sternal:</strong> Extension (to ~120°), adduction, horizontal adduction, medial rotation',
        'Chapter 13: Pec Major Multi-Actions'
    ]
))

deck.add_note(genanki.Note(
    model=cloze_model,
    fields=[
        'The clavicular portion of pectoralis major performs {{c1::flexion}} (to ~60°), {{c2::horizontal adduction}}, and {{c3::medial rotation}}.',
        '',
        'Chapter 13: Pec Major Clavicular'
    ]
))

deck.add_note(genanki.Note(
    model=cloze_model,
    fields=[
        'The sternal portion of pectoralis major performs {{c1::extension}} (to ~120°), {{c2::adduction}}, {{c3::horizontal adduction}}, and {{c4::medial rotation}}.',
        '',
        'Chapter 13: Pec Major Sternal'
    ]
))

# Comparison: Pec Major Portions
deck.add_note(genanki.Note(
    model=comparison_model,
    fields=[
        'Pectoralis Major: Clavicular vs. Sternal portions',
        '<strong>Clavicular Portion:</strong><ul><li>Flexion (to ~60°)</li><li>Horizontal adduction</li><li>Medial rotation</li></ul><strong>Sternal Portion:</strong><ul><li>Extension (to ~120°)</li><li>Adduction</li><li>Horizontal adduction</li><li>Medial rotation</li></ul><div class="emphasis">Both: Horizontal adduction and medial rotation</div>',
        'Chapter 13: Pec Major Comparison'
    ]
))

# Rotator Cuff - SITS Muscles
deck.add_note(genanki.Note(
    model=basic_model,
    fields=[
        'What are the four rotator cuff (SITS) muscles?',
        '<ul><li><strong>S</strong>upraspinatus</li><li><strong>I</strong>nfraspinatus</li><li><strong>T</strong>eres minor</li><li><strong>S</strong>ubscapularis</li></ul>',
        'Chapter 13: Rotator Cuff'
    ]
))

deck.add_note(genanki.Note(
    model=cloze_model,
    fields=[
        'The rotator cuff (SITS) muscles are {{c1::Supraspinatus}}, {{c2::Infraspinatus}}, {{c3::Teres minor}}, and {{c4::Subscapularis}}.',
        '',
        'Chapter 13: SITS'
    ]
))

# Supraspinatus
deck.add_note(genanki.Note(
    model=basic_reverse_model,
    fields=[
        'Supraspinatus',
        'Actions:<br>- Abduction (initiates first 15-30°)<br>- Stabilizes humeral head',
        'Chapter 13: Rotator Cuff'
    ]
))

deck.add_note(genanki.Note(
    model=cloze_model,
    fields=[
        'Supraspinatus {{c1::initiates abduction}} and {{c2::stabilizes the humeral head}}.',
        '',
        'Chapter 13: Supraspinatus'
    ]
))

# Infraspinatus
deck.add_note(genanki.Note(
    model=basic_reverse_model,
    fields=[
        'Infraspinatus',
        'Actions:<br>- Lateral rotation<br>- Horizontal abduction<br>- Stabilizes humeral head',
        'Chapter 13: Rotator Cuff'
    ]
))

deck.add_note(genanki.Note(
    model=cloze_model,
    fields=[
        'Infraspinatus performs {{c1::lateral rotation}}, {{c2::horizontal abduction}}, and {{c3::stabilization}} of the humeral head.',
        '',
        'Chapter 13: Infraspinatus'
    ]
))

# Teres Minor
deck.add_note(genanki.Note(
    model=basic_reverse_model,
    fields=[
        'Teres Minor',
        'Actions:<br>- Lateral rotation<br>- Horizontal abduction<br>- Stabilizes humeral head',
        'Chapter 13: Rotator Cuff'
    ]
))

deck.add_note(genanki.Note(
    model=cloze_model,
    fields=[
        'Teres minor performs {{c1::lateral rotation}}, {{c2::horizontal abduction}}, and {{c3::stabilization}} of the humeral head.',
        '',
        'Chapter 13: Teres Minor'
    ]
))

# Subscapularis
deck.add_note(genanki.Note(
    model=basic_reverse_model,
    fields=[
        'Subscapularis',
        'Actions:<br>- Medial rotation<br>- Anterior stabilization of humeral head',
        'Chapter 13: Rotator Cuff'
    ]
))

deck.add_note(genanki.Note(
    model=cloze_model,
    fields=[
        'Subscapularis performs {{c1::medial rotation}} and {{c2::anterior stabilization}} of the humeral head.',
        '',
        'Chapter 13: Subscapularis'
    ]
))

# Comparison: Infraspinatus vs Teres Minor vs Subscapularis
deck.add_note(genanki.Note(
    model=comparison_model,
    fields=[
        'Rotator Cuff Rotation Actions',
        '<strong>Lateral Rotators:</strong><ul><li>Infraspinatus</li><li>Teres minor</li></ul><strong>Medial Rotator:</strong><ul><li>Subscapularis</li></ul><div class="emphasis">Both infraspinatus and teres minor also perform horizontal abduction</div>',
        'Chapter 13: Rotator Cuff Rotations'
    ]
))

# Latissimus Dorsi and Teres Major
deck.add_note(genanki.Note(
    model=basic_reverse_model,
    fields=[
        'Latissimus Dorsi',
        'Actions:<br>- Extension<br>- Adduction<br>- Medial rotation',
        'Chapter 13: Latissimus Dorsi'
    ]
))

deck.add_note(genanki.Note(
    model=basic_reverse_model,
    fields=[
        'Teres Major',
        'Actions:<br>- Extension<br>- Adduction<br>- Medial rotation',
        'Chapter 13: Teres Major'
    ]
))

deck.add_note(genanki.Note(
    model=cloze_model,
    fields=[
        'Both {{c1::latissimus dorsi}} and {{c2::teres major}} perform shoulder extension, adduction, and medial rotation.',
        '',
        'Chapter 13: Lat and Teres Major'
    ]
))

# ============================================================================
# CLINICAL PEARLS
# ============================================================================

# Scapulohumeral Rhythm
deck.add_note(genanki.Note(
    model=clinical_model,
    fields=[
        'What is the scapulohumeral rhythm ratio?',
        'For every 2° of shoulder abduction/flexion:<ul><li>1° occurs at glenohumeral joint</li><li>1° occurs at scapulothoracic joint</li></ul><div class="emphasis">Ratio: 2:1 (GH:ST)</div>',
        'This describes the coordinated movement between the humerus and scapula',
        'Clinical Pearls: Scapulohumeral Rhythm'
    ]
))

deck.add_note(genanki.Note(
    model=cloze_model,
    fields=[
        'The scapulohumeral rhythm is a {{c1::2:1}} ratio, where for every {{c2::2}}° of shoulder movement, {{c3::1}}° occurs at the glenohumeral joint and {{c4::1}}° occurs at the scapulothoracic joint.',
        '',
        'Clinical Pearls: Scapulohumeral Rhythm'
    ]
))

# Force Couple - Shoulder Abduction
deck.add_note(genanki.Note(
    model=clinical_model,
    fields=[
        'What is the force couple for shoulder abduction?',
        '<ul><li>Deltoid (produces upward force)</li><li>Rotator cuff muscles (stabilize humeral head in glenoid)</li></ul>',
        'The rotator cuff prevents superior translation of the humeral head while the deltoid abducts',
        'Clinical Pearls: Shoulder Force Couple'
    ]
))

deck.add_note(genanki.Note(
    model=cloze_model,
    fields=[
        'The shoulder abduction force couple consists of the {{c1::deltoid}} producing upward force and the {{c2::rotator cuff}} stabilizing the humeral head.',
        '',
        'Clinical Pearls: Shoulder Abduction'
    ]
))

# Scapular Force Couples Summary
deck.add_note(genanki.Note(
    model=clinical_model,
    fields=[
        'What are the six scapular force couples?',
        '<ul><li>Upward rotation: Serratus anterior + Lower/Upper Trapezius (SLUT)</li><li>Downward rotation: Pectoralis minor + Rhomboids + Levator scapulae (PRL)</li><li>Retraction: Trapezius (all) + Rhomboids</li><li>Protraction: Serratus anterior + Pectoralis minor</li><li>Elevation: Upper trapezius + Levator scapulae + Rhomboids</li><li>Depression: Lower trapezius + Pectoralis minor</li></ul>',
        '',
        'Clinical Pearls: Scapular Force Couples'
    ]
))

# Postural Muscles
deck.add_note(genanki.Note(
    model=clinical_model,
    fields=[
        'Which muscles maintain the cervical lordosis?',
        '<ul><li>Suboccipital extensors</li><li>Splenius</li></ul>',
        'These muscles work to maintain the natural curve',
        'Clinical Pearls: Cervical Posture'
    ]
))

deck.add_note(genanki.Note(
    model=clinical_model,
    fields=[
        'Which muscles maintain the lumbar lordosis?',
        '<ul><li>Erector spinae</li><li>Multifidus</li></ul>',
        'These muscles work to maintain the natural curve',
        'Clinical Pearls: Lumbar Posture'
    ]
))

deck.add_note(genanki.Note(
    model=cloze_model,
    fields=[
        'The {{c1::erector spinae}} counters forward flexion at the thoracic spine to maintain proper {{c2::thoracic kyphosis}}.',
        '',
        'Clinical Pearls: Thoracic Posture'
    ]
))

# Additional key clinical cards for bilateral/unilateral concepts
deck.add_note(genanki.Note(
    model=clinical_model,
    fields=[
        'What is the difference between ipsilateral and contralateral muscle actions?',
        '<strong>Ipsilateral (same side):</strong><br>Muscle on right side produces movement to the right<br>Examples: Internal oblique rotation, Splenius rotation<br><br><strong>Contralateral (opposite side):</strong><br>Muscle on right side produces movement to the left<br>Examples: External oblique rotation, SCM rotation, Transversospinalis rotation',
        '',
        'Clinical Pearls: Action Specificity'
    ]
))

deck.add_note(genanki.Note(
    model=cloze_model,
    fields=[
        '{{c1::Ipsilateral}} means same side, where a muscle on the right produces movement to the right. {{c2::Contralateral}} means opposite side, where a muscle on the right produces movement to the left.',
        '',
        'Clinical Pearls: Terminology'
    ]
))

# Summary card for key rotation patterns
deck.add_note(genanki.Note(
    model=clinical_model,
    fields=[
        'Summary: Which muscles rotate to the SAME side vs. OPPOSITE side?',
        '<strong>SAME SIDE (Ipsilateral):</strong><ul><li>Internal oblique</li><li>Splenius/Splenii</li><li>Splenius cervicis</li></ul><strong>OPPOSITE SIDE (Contralateral):</strong><ul><li>External oblique</li><li>Sternocleidomastoid</li><li>Transversospinalis</li></ul>',
        'Critical pattern to remember!',
        'Clinical Pearls: Rotation Patterns'
    ]
))

print(f"Created {len(deck.notes)} cards in the anatomy deck!")

# Write deck to file
output_file = 'Anatomy_Unit2_Comprehensive.apkg'
genanki.Package(deck).write_to_file(output_file)
print(f"Deck successfully exported to {output_file}")
print(f"\nTo use: Import the .apkg file into Anki using File -> Import")
