"""
populate_mock_tests_30.py — Populate comprehensive mock tests with 30 questions each
Run this after running the app once to set up the database.
"""

import sqlite3
from database import get_db

def add_questions(conn, test_id, questions_data):
    """Helper function to add questions to a test"""
    c = conn.cursor()
    for order, q_data in enumerate(questions_data, 1):
        q_id = c.execute(
            """INSERT INTO questions (mock_test_id, question_text, question_type, 
               marks, question_order)
               VALUES (?, ?, ?, ?, ?)""",
            (test_id, q_data['text'], 'MCQ', 1, order)
        ).lastrowid
        
        for opt_order, option_text in enumerate(q_data['options']):
            is_correct = 1 if opt_order == q_data['correct'] else 0
            c.execute(
                """INSERT INTO options (question_id, option_text, option_order, is_correct)
                   VALUES (?, ?, ?, ?)""",
                (q_id, option_text, opt_order, is_correct)
            )

def populate_sample_tests():
    conn = get_db()
    c = conn.cursor()
    
    existing_titles = {row[0] for row in c.execute("SELECT title FROM mock_tests").fetchall()}
    
    def insert_test(title, description, subject, exam_type, total_questions, duration, difficulty_level):
        if title in existing_titles:
            return None
        test_id = c.execute(
            """INSERT INTO mock_tests (title, description, subject, exam_type, 
               total_questions, duration, difficulty_level)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (title, description, subject, exam_type, total_questions, duration, difficulty_level)
        ).lastrowid
        existing_titles.add(title)
        return test_id
    
    tests_info = []
    
    # ═══════════════════════════════════════════════════════════════════
    # JEE MAIN TESTS
    # ═══════════════════════════════════════════════════════════════════
    
    # JEE Main - Physics
    test_id = insert_test(
        'JEE Main - Physics', 'Complete Physics mock test for JEE Main', 
        'Physics', 'JEE Main', 30, 60, 'Medium'
    )
    if test_id:
        tests_info.append(('JEE Main - Physics', test_id))
    
    jee_physics = [
        {'text': 'What is the SI unit of force?', 'options': ['Newton', 'Dyne', 'Joule', 'Pascal'], 'correct': 0},
        {'text': 'Calculate the acceleration due to gravity at height = Earth\'s radius', 'options': ['2.45 m/s²', '4.9 m/s²', '9.8 m/s²', '1.23 m/s²'], 'correct': 0},
        {'text': 'Kinetic energy of 2kg object moving at 5 m/s is?', 'options': ['25 J', '50 J', '100 J', '10 J'], 'correct': 0},
        {'text': 'Gravitational potential energy is?', 'options': ['-GMm/r', 'GMm/r²', 'GMm/r', 'GMm/2r'], 'correct': 0},
        {'text': 'A ball thrown vertically upward reaches max height in 2 sec. Initial velocity is?', 'options': ['20 m/s', '19.6 m/s', '10 m/s', '5 m/s'], 'correct': 1},
        {'text': 'Coefficient of restitution ranges from?', 'options': ['0 to 1', '-1 to 0', '0 to 2', '-1 to 1'], 'correct': 0},
        {'text': 'Angular velocity is related to linear velocity by?', 'options': ['v = ωr', 'v = ω/r', 'v = r/ω', 'v = ω + r'], 'correct': 0},
        {'text': 'Moment of inertia of sphere about diameter?', 'options': ['2/5 MR²', '1/2 MR²', '2/3 MR²', '1/3 MR²'], 'correct': 0},
        {'text': 'Simple harmonic motion equation is?', 'options': ['x = A sin(ωt + φ)', 'x = At²', 'x = vt', 'x = at²/2'], 'correct': 0},
        {'text': 'Frequency of LC circuit is?', 'options': ['1/(2π√LC)', '2π√LC', '√LC', '1/√LC'], 'correct': 0},
        {'text': 'Work done by conservative force is', 'options': ['Path dependent', 'Path independent', 'Zero always', 'Negative'], 'correct': 1},
        {'text': 'Center of mass depends on', 'options': ['Shape', 'Position only', 'Arrangement and position', 'Velocity'], 'correct': 2},
        {'text': 'Rotational inertia dimension is', 'options': ['ML²T⁻²', 'ML²', 'MLT⁻¹', 'M²L'], 'correct': 1},
        {'text': 'Torque = Force × ?', 'options': ['Distance', 'Perpendicular distance', 'Mass', 'Velocity'], 'correct': 1},
        {'text': 'Angular momentum L = ?', 'options': ['Iω', 'Iα', 'Στ', 'Fv'], 'correct': 0},
        {'text': 'Precession angle depends on', 'options': ['Angular velocity', 'Mass', 'Weight/Angular velocity', 'Radius'], 'correct': 2},
        {'text': 'Elastic collision conserves', 'options': ['Momentum only', 'KE only', 'Both momentum and KE', 'PE only'], 'correct': 2},
        {'text': 'Stress = ?', 'options': ['Force/Area', 'Strain/Displacement', 'Area/Force', 'Displacement/Length'], 'correct': 0},
        {'text': 'Young\'s modulus = ?', 'options': ['Stress/Strain', 'Strain/Stress', 'Stress × Strain', 'Stress + Strain'], 'correct': 0},
        {'text': 'Surface tension acts', 'options': ['Perpendicular to surface', 'Parallel to surface', 'At 45°', 'Inside liquid'], 'correct': 1},
        {'text': 'Viscosity coefficient unit = ?', 'options': ['N·s/m²', 'N/m²', 'N·m', 'N·s'], 'correct': 0},
        {'text': 'Stokes law F = ?', 'options': ['6πηrv', '3πηrv', 'πηrv', '4πηrv'], 'correct': 0},
        {'text': 'Bulk modulus related to', 'options': ['Volume change', 'Length change', 'Surface change', 'Mass change'], 'correct': 0},
        {'text': 'Shear modulus = ?', 'options': ['Shear stress/Shear strain', 'Stress × Strain', 'Normal stress/Strain', 'Lateral strain/Longitudinal'], 'correct': 0},
        {'text': 'Density of water at 4°C = ?', 'options': ['1000 kg/m³', '1 g/cm³', 'Both', 'Less than 1 g/cm³'], 'correct': 2},
        {'text': 'Archimedes principle states', 'options': ['Buoyant force = Weight', 'Buoyant force = Weight of fluid displaced', 'Pressure at depth', 'Velocity in fluids'], 'correct': 1},
        {'text': 'Continuity equation is', 'options': ['A1v1 = A2v2', 'A1/v1 = A2/v2', 'A1v1² = A2v2²', 'A1 + A2 = v1 + v2'], 'correct': 0},
        {'text': 'Bernoulli equation relates', 'options': ['Pressure and velocity', 'Height and velocity', 'Pressure, height and velocity', 'Temperature and pressure'], 'correct': 2},
        {'text': 'Poiseuille\'s formula for flow rate Q = ?', 'options': ['πPr⁴/8η', '8πPr⁴/η', 'Pr⁴/8πη', 'πr⁴/Pη'], 'correct': 0},
        {'text': 'Reynolds number helps determine', 'options': ['Laminar flow', 'Turbulent flow', 'Type of flow', 'Pressure drop'], 'correct': 2},
    ]
    add_questions(conn, test_id, jee_physics)
    
    # JEE Main - Chemistry
    test_id = insert_test(
        'JEE Main - Chemistry', 'Complete Chemistry mock test for JEE Main', 
        'Chemistry', 'JEE Main', 30, 60, 'Medium'
    )
    if test_id:
        tests_info.append(('JEE Main - Chemistry', test_id))
    
    jee_chemistry = [
        {'text': 'Atomic number of Carbon?', 'options': ['4', '6', '8', '12'], 'correct': 1},
        {'text': 'Electron configuration of Cu²⁺ is?', 'options': ['[Ar] 3d⁹', '[Ar] 3d⁸ 4s¹', '[Ar] 3d⁸', '[Ar] 3d¹⁰'], 'correct': 2},
        {'text': 'Bond energy is highest in?', 'options': ['N≡N', 'N-N', 'N=N', 'N-O'], 'correct': 0},
        {'text': 'Hybridization in NH3?', 'options': ['sp', 'sp²', 'sp³', 'sp³d'], 'correct': 2},
        {'text': 'pH of 0.1 M HCl?', 'options': ['0.5', '1', '2', '-1'], 'correct': 1},
        {'text': 'Rate law for first order reaction?', 'options': ['k = ln([A]₀/[A])', 'k = t', 'k = [A]', 'k = [A]²'], 'correct': 0},
        {'text': 'In SN2 reaction, inversion occurs?', 'options': ['100%', '50%', '25%', '75%'], 'correct': 0},
        {'text': 'Benzene is aromatic due to?', 'options': ['Conjugation', 'Planarity', 'Hückel rule', 'All'], 'correct': 3},
        {'text': 'Oxidation state of S in H2SO4?', 'options': ['+4', '+6', '+2', '+8'], 'correct': 1},
        {'text': 'Electronegativity increases in?', 'options': ['Left to right', 'Top to bottom', 'Left to bottom', 'Right to bottom'], 'correct': 0},
        {'text': 'Ionic bond is formed between?', 'options': ['Non-metal and non-metal', 'Metal and non-metal', 'Metal and metal', 'All'], 'correct': 1},
        {'text': 'VSEPR theory predicts molecular', 'options': ['Shape', 'Color', 'Density', 'Conductivity'], 'correct': 0},
        {'text': 'Resonance occurs when', 'options': ['Multiple structures exist', 'Lone pairs present', 'Double bonds exist', 'Charged atoms present'], 'correct': 0},
        {'text': 'Coordinate covalent bond needs', 'options': ['Shared pair from both', 'Shared pair from one', 'Transfer of electrons', 'Loss of electrons'], 'correct': 1},
        {'text': 'Hydration enthalpy is', 'options': ['Endothermic', 'Exothermic', 'Zero', 'Temperature dependent'], 'correct': 1},
        {'text': 'Lattice enthalpy is highest for', 'options': ['NaCl', 'KCl', 'LiF', 'CsI'], 'correct': 2},
        {'text': 'Entropy increases when', 'options': ['Order increases', 'Disorder increases', 'Temperature decreases', 'Pressure increases'], 'correct': 1},
        {'text': 'Spontaneous reaction requires', 'options': ['ΔG > 0', 'ΔG < 0', 'ΔH > 0', 'ΔS > 0'], 'correct': 1},
        {'text': 'Van der Waals forces are', 'options': ['Strong', 'Weak', 'Medium', 'Variable'], 'correct': 1},
        {'text': 'Dipole-dipole forces exist in', 'options': ['HF', 'Cl2', 'H2', 'CH4'], 'correct': 0},
        {'text': 'Quantum number n determines', 'options': ['Shape', 'Energy level', 'Orientation', 'Spin'], 'correct': 1},
        {'text': 'Quantum number l determines', 'options': ['Energy', 'Shape of orbital', 'Orientation', 'Spin'], 'correct': 1},
        {'text': 'Quantum number ml determines', 'options': ['Energy', 'Shape', 'Orientation', 'Spin'], 'correct': 2},
        {'text': 'Pauli exclusion principle states', 'options': ['One orbital per electron', 'No two electrons with same quantum numbers', 'Electrons fill lowest first', 'Maximum 8 electrons'], 'correct': 1},
        {'text': 'Hund\'s rule states electrons', 'options': ['Pair up first', 'Fill singly first', 'Fill randomly', 'Fill from outside'], 'correct': 1},
        {'text': 'Ground state electron config of N?', 'options': ['1s² 2s² 2p²', '1s² 2s² 2p³', '1s² 2s¹ 2p⁴', '1s² 2s³'], 'correct': 1},
        {'text': 'Ionization energy trend increases', 'options': ['Down group', 'Across period', 'Inside to outside', 'Variable'], 'correct': 1},
        {'text': 'Electron affinity is usually', 'options': ['Positive', 'Negative', 'Zero', 'Depends on element'], 'correct': 1},
        {'text': 'Metallic character increases', 'options': ['Left to right', 'Right to left', 'Top to bottom', 'Inside to outside'], 'correct': 1},
        {'text': 'Non-metallic character increases', 'options': ['Down the group', 'Up the group', 'Left to right', 'Depends on block'], 'correct': 2},
    ]
    add_questions(conn, test_id, jee_chemistry)
    
    # JEE Main - Mathematics
    test_id = insert_test(
        'JEE Main - Mathematics', 'Complete Mathematics mock test for JEE Main', 
        'Mathematics', 'JEE Main', 30, 60, 'Medium'
    )
    if test_id:
        tests_info.append(('JEE Main - Mathematics', test_id))
    
    jee_math = [
        {'text': 'If sin(θ) = 3/5, then cos(θ) = ?', 'options': ['4/5', '3/4', '5/4', '-4/5'], 'correct': 0},
        {'text': 'Derivative of x³ + 2x² + x is?', 'options': ['3x² + 4x + 1', '3x + 4', 'x² + 2x', 'x³ + 4x'], 'correct': 0},
        {'text': '∫x² dx = ?', 'options': ['x³/3 + C', 'x³ + C', '2x + C', 'x² + C'], 'correct': 0},
        {'text': 'Distance from point (1,2) to line x + y + 1 = 0 is?', 'options': ['√2', '2√2', '1', '√2/2'], 'correct': 1},
        {'text': 'Sum of first n natural numbers = ?', 'options': ['n(n+1)/2', 'n²', 'n(n+1)', 'n²/2'], 'correct': 0},
        {'text': 'In matrix multiplication AB, #columns in A = ?', 'options': ['#rows in B', '#columns in B', '#rows in A', '#rows in result'], 'correct': 0},
        {'text': 'Probability of getting 2 heads in 3 coin tosses = ?', 'options': ['1/8', '3/8', '1/2', '1/4'], 'correct': 1},
        {'text': 'If A + B = π/2, then tan(A+B) = ?', 'options': ['1', 'undefined', '0', '-1'], 'correct': 1},
        {'text': 'Area of circle with radius r = ?', 'options': ['πr²', '2πr', 'πr', 'πr²/2'], 'correct': 0},
        {'text': 'Number of permutations of 5 objects taken 3 at a time = ?', 'options': ['60', '10', '120', '20'], 'correct': 0},
        {'text': 'tan(A+B) = ?', 'options': ['(tanA+tanB)/(1-tanAtanB)', '(tanA-tanB)/(1+tanAtanB)', 'tanA + tanB', 'tanA - tanB'], 'correct': 0},
        {'text': 'cos(2θ) = ?', 'options': ['2cos²θ - 1', 'cos²θ - sin²θ', '1 - 2sin²θ', 'All'], 'correct': 3},
        {'text': 'sin(3θ) = ?', 'options': ['3sinθ - 4sin³θ', '3sinθ + 4sin³θ', '4sin³θ - 3sinθ', 'sin³θ'], 'correct': 0},
        {'text': 'Limit of (sin x)/x as x→0 = ?', 'options': ['0', '1', 'undefined', 'infinity'], 'correct': 1},
        {'text': 'Second derivative test for maxima?', 'options': ['f\'(x)=0, f\'\'(x)<0', 'f\'(x)=0, f\'\'(x)>0', 'f\'(x)>0', 'f\'(x)<0'], 'correct': 0},
        {'text': '∫e^x dx = ?', 'options': ['e^x', 'e^x + C', 'e^(x+1)/(x+1)', 'xe^x'], 'correct': 1},
        {'text': '∫1/x dx = ?', 'options': ['-1/x²', 'ln|x| + C', '1/x²', 'x'], 'correct': 1},
        {'text': 'Equation of circle with center (h,k) and radius r?', 'options': ['(x-h)² + (y-k)² = r²', 'x² + y² = r²', '(x+h)² + (y+k)² = r', '(x-h)(y-k) = r'], 'correct': 0},
        {'text': 'Eccentricity of ellipse e = ?', 'options': ['√(1-b²/a²)', 'a²/b²', 'b/a', 'a/b'], 'correct': 0},
        {'text': 'Eccentricity of hyperbola e = ?', 'options': ['√(1+b²/a²)', '√(1-b²/a²)', 'b/a', 'a/b'], 'correct': 0},
        {'text': 'Determinant of 2×2 matrix [[a,b],[c,d]] = ?', 'options': ['ad + bc', 'ad - bc', 'ab - cd', 'ac - bd'], 'correct': 1},
        {'text': 'Inverse of matrix A = ?', 'options': ['1/A', 'adj(A)/det(A)', 'A/det(A)', 'det(A)/adj(A)'], 'correct': 1},
        {'text': 'Rank of matrix is', 'options': ['Number of rows', 'Number of columns', 'Dimension of row/column space', 'Sum of diagonal'], 'correct': 2},
        {'text': 'If roots of ax²+bx+c are α,β then α+β = ?', 'options': ['-b/a', 'b/a', 'c/a', '-c/a'], 'correct': 0},
        {'text': 'If roots of ax²+bx+c are α,β then αβ = ?', 'options': ['-b/a', 'b/a', 'c/a', '-c/a'], 'correct': 2},
        {'text': 'General term of AP = ?', 'options': ['a + nd', 'a + (n-1)d', 'a(1+r)^(n-1)', 'an + b'], 'correct': 1},
        {'text': 'General term of GP = ?', 'options': ['a + nd', 'a + (n-1)d', 'ar^(n-1)', 'a(r-1)'], 'correct': 2},
        {'text': 'Sum of infinite GP |r|<1 = ?', 'options': ['a/(1-r)', 'ar/(1-r)', 'a(1-r)', 'a/(1+r)'], 'correct': 0},
        {'text': 'Principle of Mathematical Induction needs', 'options': ['Base case only', 'Inductive step only', 'Base case and inductive step', 'Hypothesis'], 'correct': 2},
        {'text': 'Binomial theorem (a+b)^n = ?', 'options': ['Σ C(n,r)a^(n-r)b^r', 'Σ C(n,r)a^r b^(n-r)', 'Σ a^n + b^n', 'C(n,r)a^n'], 'correct': 0},
    ]
    add_questions(conn, test_id, jee_math)
    
    # ═══════════════════════════════════════════════════════════════════
    # NEET TESTS
    # ═══════════════════════════════════════════════════════════════════
    
    # NEET - Biology
    test_id = insert_test(
        'NEET - Biology', 'Complete Biology mock test for NEET', 
        'Biology', 'NEET', 30, 90, 'Hard'
    )
    if test_id:
        tests_info.append(('NEET - Biology', test_id))
    
    neet_bio = [
        {'text': 'Basic unit of life is?', 'options': ['Atom', 'Molecule', 'Cell', 'Nucleus'], 'correct': 2},
        {'text': 'Photosynthesis mainly occurs in?', 'options': ['Root', 'Stem', 'Leaf', 'Flower'], 'correct': 2},
        {'text': 'Chromosomes in human cell = ?', 'options': ['23', '46', '48', '50'], 'correct': 1},
        {'text': 'DNA structure discovered by?', 'options': ['Mendel', 'Darwin', 'Watson & Crick', 'Pasteur'], 'correct': 2},
        {'text': 'Mitochondria is known as?', 'options': ['Powerhouse of cell', 'Protein factory', 'Energy storage', 'Waste dump'], 'correct': 0},
        {'text': 'Process of protein synthesis = ?', 'options': ['Transcription', 'Translation', 'Replication', 'Mutation'], 'correct': 1},
        {'text': 'Enzyme that cuts DNA = ?', 'options': ['Ligase', 'Polymerase', 'Restriction enzyme', 'Helicase'], 'correct': 2},
        {'text': 'Blood group AB means?', 'options': ['No antigen', 'A and B antigens', 'O antigen', 'Rh antigen'], 'correct': 1},
        {'text': 'Stomata found in plants helps in?', 'options': ['Water absorption', 'Gas exchange', 'Nutrient transport', 'Support'], 'correct': 1},
        {'text': 'Dominant trait appears when?', 'options': ['Heterozygous', 'Homozygous', 'Both', 'Neither'], 'correct': 0},
        {'text': 'Glycolysis occurs in?', 'options': ['Mitochondria', 'Cytoplasm', 'Chloroplast', 'Nucleus'], 'correct': 1},
        {'text': 'Krebs cycle occurs in?', 'options': ['Cytoplasm', 'Inner membrane', 'Matrix', 'Outer membrane'], 'correct': 2},
        {'text': 'ATP is produced in?', 'options': ['Ribosomes', 'Lysosomes', 'Mitochondria', 'Golgi'], 'correct': 2},
        {'text': 'Photosynthesis equation is', 'options': ['6CO2 + 6H2O → C6H12O6 + 6O2', 'C6H12O6 → 2C2H5OH', 'CO2 → Glucose', 'H2O → O2 + H'], 'correct': 0},
        {'text': 'Light reactions occur in?', 'options': ['Stroma', 'Thylakoid', 'Cytoplasm', 'Vacuole'], 'correct': 1},
        {'text': 'Dark reactions occur in?', 'options': ['Thylakoid', 'Stroma', 'Grana', 'Lumen'], 'correct': 1},
        {'text': 'Calvin cycle is also known as?', 'options': ['Light reaction', 'Dark reaction', 'Photolysis', 'Glycolysis'], 'correct': 1},
        {'text': 'Meiosis produces?', 'options': ['2 cells', '4 cells', '8 cells', 'Many cells'], 'correct': 1},
        {'text': 'Mitosis produces?', 'options': ['2 cells', '4 cells', '8 cells', 'Many cells'], 'correct': 0},
        {'text': 'Homologous chromosomes pair during?', 'options': ['Prophase II', 'Prophase I', 'Metaphase', 'Anaphase'], 'correct': 1},
        {'text': 'Crossing over occurs during?', 'options': ['Prophase I', 'Metaphase I', 'Anaphase I', 'Telophase'], 'correct': 0},
        {'text': 'Genotype frequency is constant in?', 'options': ['Hardy-Weinberg equilibrium', 'Evolution', 'Mutation', 'Selection'], 'correct': 0},
        {'text': 'Allele frequency can change due to?', 'options': ['Mutation', 'Gene flow', 'Drift', 'All'], 'correct': 3},
        {'text': 'Natural selection favors', 'options': ['Weaker organisms', 'Stronger organisms', 'Best adapted organisms', 'Random'], 'correct': 2},
        {'text': 'Adaptation is result of?', 'options': ['Inheritance', 'Use and disuse', 'Natural selection', 'Environment'], 'correct': 2},
        {'text': 'Vestigial organs are evidence of?', 'options': ['Creation', 'Evolution', 'Adaptation', 'Mutation'], 'correct': 1},
        {'text': 'DNA replication is', 'options': ['Conservative', 'Semiconservative', 'Dispersive', 'Non-conservative'], 'correct': 1},
        {'text': 'DNA polymerase adds bases in', 'options': ['5\' to 3\'', '3\' to 5\'', 'Both directions', 'Random'], 'correct': 0},
        {'text': 'Okazaki fragments are found in', 'options': ['Leading strand', 'Lagging strand', 'Both', 'Origin'], 'correct': 1},
        {'text': 'Telomere protects', 'options': ['Gene', 'Chromosome end', 'Centromere', 'Spindle'], 'correct': 1},
    ]
    add_questions(conn, test_id, neet_bio)
    
    # NEET - Chemistry
    test_id = insert_test(
        'NEET - Chemistry', 'Complete Chemistry mock test for NEET', 
        'Chemistry', 'NEET', 30, 90, 'Hard'
    )
    if test_id:
        tests_info.append(('NEET - Chemistry', test_id))
    
    neet_chem = [
        {'text': 'Atomic mass of Carbon = ?', 'options': ['12', '6', '14', '18'], 'correct': 0},
        {'text': 'Molar mass of H2SO4 = ?', 'options': ['94', '98', '102', '96'], 'correct': 1},
        {'text': 'Oxidation state of O in H2O2 = ?', 'options': ['-1', '-2', '+1', '+2'], 'correct': 0},
        {'text': 'pH + pOH = ?', 'options': ['7', '14', '0', '21'], 'correct': 1},
        {'text': 'Boiling point increases with?', 'options': ['Ionic bonding', 'Hydrogen bonding', 'Van der Waals', 'Metallic bonding'], 'correct': 1},
        {'text': 'Allotrope of Carbon?', 'options': ['Graphite', 'Diamond', 'Buckminsterfullerene', 'All'], 'correct': 3},
        {'text': 'Halogens are in which group?', 'options': ['16', '17', '18', '1'], 'correct': 1},
        {'text': 'Noble gases are in which group?', 'options': ['17', '18', '1', '2'], 'correct': 1},
        {'text': 'Alkanes general formula = ?', 'options': ['CnH2n+2', 'CnH2n', 'CnHn', 'CnH2n-2'], 'correct': 0},
        {'text': 'Carboxylic acid group = ?', 'options': ['-OH', '-CHO', '-COOH', '-COO'], 'correct': 2},
        {'text': 'Alcohol group = ?', 'options': ['-OH', '-CHO', '-COOH', '-COO'], 'correct': 0},
        {'text': 'Ether group = ?', 'options': ['-O-', '=O', '-OH', '-OOH'], 'correct': 0},
        {'text': 'Ketone contains', 'options': ['CHO', 'CO between carbons', 'COOH', 'OH'], 'correct': 1},
        {'text': 'Amine group = ?', 'options': ['-NH2', '-OH', '-COOH', '-SH'], 'correct': 0},
        {'text': 'Thiol group = ?', 'options': ['-NH2', '-OH', '-SH', '-S-'], 'correct': 2},
        {'text': 'Isomerism is possible in', 'options': ['Alkanes', 'Alkenes', 'Alkynes', 'All'], 'correct': 3},
        {'text': 'Geometrical isomerism requires', 'options': ['Single bond', 'Double bond', 'Restricted rotation', 'Both B and C'], 'correct': 3},
        {'text': 'Optical isomerism needs', 'options': ['Chiral center', 'Double bond', 'Functional group', 'Chain'], 'correct': 0},
        {'text': 'Catalytic cracking produces', 'options': ['Smaller alkanes', 'Alkenes', 'Both', 'Aromatics'], 'correct': 2},
        {'text': 'Polymerization is', 'options': ['Addition', 'Condensation', 'Both', 'Elimination'], 'correct': 2},
        {'text': 'Addition polymerization forms', 'options': ['Nylon', 'PVC', 'Rubber', 'All'], 'correct': 2},
        {'text': 'Condensation polymerization needs', 'options': ['Functional groups', 'Water removal', 'Both', 'Heat'], 'correct': 2},
        {'text': 'Macromolecules include', 'options': ['Proteins', 'Carbohydrates', 'Lipids', 'All'], 'correct': 3},
        {'text': 'Proteins are made of', 'options': ['Amino acids', 'Glucose', 'Fatty acids', 'Nucleotides'], 'correct': 0},
        {'text': 'Carbohydrates general formula', 'options': ['Cn(H2O)m', 'CnH2nOn', 'CnHm', 'All'], 'correct': 0},
        {'text': 'Lipids are', 'options': ['Hydrophilic', 'Hydrophobic', 'Polar', 'Charged'], 'correct': 1},
        {'text': 'Nucleic acids contain', 'options': ['C, H, O', 'C, H, O, N', 'C, H, O, N, P', 'C, H, O, N, S'], 'correct': 2},
        {'text': 'DNA base pairs are', 'options': ['A-U', 'G-C', 'A-T, G-C', 'A-G'], 'correct': 2},
        {'text': 'RNA contains', 'options': ['Deoxyribose', 'Ribose', 'Glucose', 'Galactose'], 'correct': 1},
        {'text': 'Double helix structure by', 'options': ['Hydrogen bonds', 'Covalent bonds', 'Ionic bonds', 'Van der Waals'], 'correct': 0},
    ]
    add_questions(conn, test_id, neet_chem)
    
    # NEET - Physics
    test_id = insert_test(
        'NEET - Physics', 'Complete Physics mock test for NEET', 
        'Physics', 'NEET', 30, 90, 'Hard'
    )
    if test_id:
        tests_info.append(('NEET - Physics', test_id))
    
    neet_phys = [
        {'text': 'Speed of light in vacuum = ?', 'options': ['3×10⁸ m/s', '3×10⁷ m/s', '3×10⁹ m/s', '3×10⁶ m/s'], 'correct': 0},
        {'text': 'Newton\'s first law is about?', 'options': ['Force', 'Inertia', 'Acceleration', 'Motion'], 'correct': 1},
        {'text': 'Power = ?', 'options': ['Force × Distance', 'Work / Time', 'Mass × Acceleration', 'Energy - Heat'], 'correct': 1},
        {'text': 'Focal length of plane mirror = ?', 'options': ['0', 'Infinity', 'Positive', 'Negative'], 'correct': 1},
        {'text': 'Snell\'s law n1 sin θ1 = ?', 'options': ['n1 sin θ2', 'n2 sin θ1', 'n2 sin θ2', 'sin θ1 + sin θ2'], 'correct': 2},
        {'text': 'Specific heat capacity unit = ?', 'options': ['J/kg', 'J/kg·K', 'J/K', 'kg·K/J'], 'correct': 1},
        {'text': 'Resistance depends on?', 'options': ['Length only', 'Area only', 'Material only', 'All'], 'correct': 3},
        {'text': 'Magnetic field lines emerge from?', 'options': ['South pole', 'North pole', 'Equator', 'Center'], 'correct': 1},
        {'text': 'Frequency unit = ?', 'options': ['Hz', 'Hertz', 'Both', 'Neither'], 'correct': 2},
        {'text': 'Doppler effect involves?', 'options': ['Sound only', 'Light only', 'Both', 'Particles only'], 'correct': 2},
        {'text': 'Wavelength × Frequency = ?', 'options': ['Velocity', 'Acceleration', 'Amplitude', 'Intensity'], 'correct': 0},
        {'text': 'Wave speed in string = ?', 'options': ['√(T/μ)', 'T×μ', 'T/μ', '√(μ/T)'], 'correct': 0},
        {'text': 'Sound speed depends on', 'options': ['Temperature only', 'Pressure only', 'Temperature and medium', 'Frequency'], 'correct': 2},
        {'text': 'Refraction occurs due to', 'options': ['Obstacle', 'Change in medium', 'Aperture', 'Resonance'], 'correct': 1},
        {'text': 'Diffraction is prominent when', 'options': ['Wavelength >> size', 'Wavelength << size', 'Size = wavelength', 'Wavelength = 0'], 'correct': 0},
        {'text': 'Interference constructive when', 'options': ['Path diff = λ/2', 'Path diff = λ', 'Path diff = 3λ/2', 'Both B and D'], 'correct': 3},
        {'text': 'Polarization shows', 'options': ['Waves are transverse', 'Waves are longitudinal', 'All waves polarize', 'Sound polarizes'], 'correct': 0},
        {'text': 'Image formed by convex lens when object at C?', 'options': ['At C', 'Between F and C', 'Between F and lens', 'At infinity'], 'correct': 0},
        {'text': 'Concave mirror forms real image when', 'options': ['Always', 'Object at infinity', 'Object beyond F', 'All'], 'correct': 2},
        {'text': 'Lens maker formula relates', 'options': ['f, R1, R2', 'n, R1, R2', 'f, n, R1, R2', 'Object distance'], 'correct': 2},
        {'text': 'Magnification by lens = ?', 'options': ['f/u', '-v/u', 'v/f', 'u/v'], 'correct': 1},
        {'text': 'Magnification by mirror = ?', 'options': ['f/u', '-v/u', 'v/f', 'u/v'], 'correct': 1},
        {'text': 'Chromatic aberration in', 'options': ['Mirror', 'Prism', 'Lens', 'Both B and C'], 'correct': 3},
        {'text': 'Angular dispersion by prism depends on', 'options': ['Angle of prism', 'Refractive index', 'Both', 'Wavelength'], 'correct': 2},
        {'text': 'Rayleigh criterion for resolution', 'options': ['θ = λ/d', 'θ = 1.22λ/d', 'θ = λd', 'θ = d/λ'], 'correct': 1},
        {'text': 'Resolving power inversely proportional to', 'options': ['λ', 'd', 'f', 'R'], 'correct': 0},
        {'text': 'Photon energy E = ?', 'options': ['hf', 'mc²', 'hc/λ', 'Both A and C'], 'correct': 3},
        {'text': 'Photoelectric effect needs', 'options': ['Intensity', 'Frequency above threshold', 'Both', 'Wave theory'], 'correct': 1},
        {'text': 'Work function is', 'options': ['Energy to remove electron', 'Kinetic energy', 'Potential energy', 'Total energy'], 'correct': 0},
        {'text': 'Stopping potential makes', 'options': ['Photocurrent zero', 'Photoelectrons fast', 'KE maximum', 'Frequency change'], 'correct': 0},
    ]
    add_questions(conn, test_id, neet_phys)
    
    # ═══════════════════════════════════════════════════════════════════
    # UPSC / CIVIL SERVICES TESTS
    # ═══════════════════════════════════════════════════════════════════
    
    # UPSC - General Studies 1
    test_id = insert_test(
        'UPSC Prelims - General Studies I', 'Civil services exam practice test', 
        'General Studies', 'UPSC', 30, 90, 'Hard'
    )
    if test_id:
        tests_info.append(('UPSC Prelims - GS I', test_id))
    
    upsc_gs1 = [
        {'text': 'Largest country by area = ?', 'options': ['Canada', 'Russia', 'China', 'USA'], 'correct': 1},
        {'text': 'Indian Constitution came into force on?', 'options': ['15 Aug 1947', '26 Jan 1950', '26 Nov 1949', '2 Oct 1869'], 'correct': 1},
        {'text': 'Capital of Australia = ?', 'options': ['Sydney', 'Melbourne', 'Canberra', 'Brisbane'], 'correct': 2},
        {'text': 'Tropic of Cancer passes through how many Indian states?', 'options': ['8', '9', '10', '11'], 'correct': 1},
        {'text': 'Which plateau covers largest area in India?', 'options': ['Chotanagpur', 'Deccan', 'Malwa', 'Mewar'], 'correct': 1},
        {'text': 'First President of Independent India = ?', 'options': ['Pandit Nehru', 'Dr. Rajendra Prasad', 'Sardar Patel', 'Maulana Abul Kalam'], 'correct': 1},
        {'text': 'Battle of Plassey was fought in year?', 'options': ['1757', '1857', '1945', '1947'], 'correct': 0},
        {'text': 'Article 1 of Indian Constitution states?', 'options': ['Right to equality', 'India is Union', 'Citizenship', 'Fundamental rights'], 'correct': 1},
        {'text': 'How many fundamental duties in Constitution?', 'options': ['9', '10', '11', '12'], 'correct': 2},
        {'text': 'Parliament of India consists of how many houses?', 'options': ['1', '2', '3', '4'], 'correct': 1},
        {'text': 'Pushpa Bhosale mountain range is in?', 'options': ['Kerala', 'Western Ghats', 'Himalayas', 'Nilgiris'], 'correct': 1},
        {'text': 'Satpura range is located in?', 'options': ['Central India', 'North India', 'South India', 'Northeast'], 'correct': 0},
        {'text': 'Eastern Ghats main range in?', 'options': ['Tamil Nadu', 'Telangana', 'Odisha', 'Andhra Pradesh'], 'correct': 2},
        {'text': 'Highest mountain peak in India = ?', 'options': ['Kangchenjunga', 'Nanda Devi', 'Kanchenjunga', 'Kanchenjunga'], 'correct': 0},
        {'text': 'Rajasthan is surrounded by?', 'options': ['4 states', '5 states', '6 states', '7 states'], 'correct': 2},
        {'text': 'River Godavari originates from?', 'options': ['Himalayas', 'Western Ghats', 'Eastern Ghats', 'Deccan'], 'correct': 1},
        {'text': 'Krishna river joins?', 'options': ['Bay of Bengal', 'Arabian Sea', 'Indian Ocean', 'Caspian'], 'correct': 0},
        {'text': 'Brahmaputra originates from?', 'options': ['Himalayas', 'Kailash', 'Myanmar', 'Tibet'], 'correct': 3},
        {'text': 'Indus river flows through?', 'options': ['India only', 'Tibet and India', 'Tibet, India, Pakistan', 'All'], 'correct': 2},
        {'text': 'Which empire built Taj Mahal?', 'options': ['Maurya', 'Mughal', 'British', 'Chola'], 'correct': 1},
        {'text': 'Ashoka was from which empire?', 'options': ['Maurya', 'Mughal', 'Gupta', 'Delhi'], 'correct': 0},
        {'text': 'Chandragupta Maurya\'s guru?', 'options': ['Kautilya', 'Arjun', 'Buddha', 'Mahavira'], 'correct': 0},
        {'text': 'Akbar\'s capital?', 'options': ['Agra', 'Delhi', 'Fatehpur Sikri', 'Lahore'], 'correct': 2},
        {'text': 'Mauryan empire capital?', 'options': ['Delhi', 'Pataliputra', 'Ujjain', 'Varanasi'], 'correct': 1},
        {'text': 'Gupta empire founded by?', 'options': ['Chandragupta I', 'Ashoka', 'Harsha', 'Vikrama'], 'correct': 0},
        {'text': 'Harsha\'s capital?', 'options': ['Ujjain', 'Kannauj', 'Mathura', 'Patna'], 'correct': 1},
        {'text': 'East India Company founded in?', 'options': ['1600', '1757', '1850', '1800'], 'correct': 0},
        {'text': 'Battle of Buxar was in?', 'options': ['1757', '1764', '1857', '1947'], 'correct': 1},
        {'text': 'Indian Rebellion year?', 'options': ['1857', '1858', '1947', '1950'], 'correct': 0},
        {'text': 'INC founded in?', 'options': ['1885', '1900', '1920', '1947'], 'correct': 0},
    ]
    add_questions(conn, test_id, upsc_gs1)
    
    # UPSC - General Studies 2
    test_id = insert_test(
        'UPSC Prelims - General Studies II', 'Civil services exam practice test', 
        'General Studies', 'UPSC', 30, 90, 'Hard'
    )
    if test_id:
        tests_info.append(('UPSC Prelims - GS II', test_id))
    
    upsc_gs2 = [
        {'text': 'UN Secretary General appoints for?', 'options': ['3 years', '5 years', '4 years', '6 years'], 'correct': 1},
        {'text': 'IMF Headquarters located in?', 'options': ['New York', 'Washington DC', 'Geneva', 'London'], 'correct': 1},
        {'text': 'WHO Headquarters in?', 'options': ['Geneva', 'New York', 'London', 'Vienna'], 'correct': 0},
        {'text': 'Right to Information Act passed in?', 'options': ['2003', '2004', '2005', '2006'], 'correct': 2},
        {'text': 'Election Commission chairman appointed for?', 'options': ['6 years', '7 years', '5 years', '8 years'], 'correct': 0},
        {'text': 'CAG tenure in office = ?', 'options': ['5 years', '6 years', '7 years', '8 years'], 'correct': 1},
        {'text': 'Lok Sabha term = ?', 'options': ['4 years', '5 years', '6 years', '3 years'], 'correct': 1},
        {'text': 'Rajya Sabha members term = ?', 'options': ['4 years', '5 years', '6 years', '8 years'], 'correct': 1},
        {'text': 'State Council of Ministers headed by?', 'options': ['Governor', 'Chief Minister', 'President', 'Deputy CM'], 'correct': 1},
        {'text': 'Total Union Territories = ?', 'options': ['6', '7', '8', '9'], 'correct': 1},
        {'text': 'Chief Justice of India appointed by?', 'options': ['President', 'Prime Minister', 'Parliament', 'Cabinet'], 'correct': 0},
        {'text': 'Supreme Court judges retire at age?', 'options': ['62', '65', '68', '70'], 'correct': 1},
        {'text': 'Number of High Courts in India = ?', 'options': ['24', '25', '26', '28'], 'correct': 2},
        {'text': 'Cabinet is responsible to?', 'options': ['President', 'Parliament', 'Lok Sabha', 'People'], 'correct': 2},
        {'text': 'No confidence motion requires?', 'options': ['1/3 members', '1/2 members', '2/3 members', '3/4 members'], 'correct': 1},
        {'text': 'Prime Minister is leader of?', 'options': ['Cabinet', 'Council of Ministers', 'Both', 'Parliament'], 'correct': 2},
        {'text': 'Vice President elected by?', 'options': ['Direct vote', 'Electoral college', 'Parliament', 'President'], 'correct': 1},
        {'text': 'Attorney General of India is?', 'options': ['Highest judge', 'Law officer', 'Legal advisor', 'Both B and C'], 'correct': 3},
        {'text': 'Comptroller and Auditor General role?', 'options': ['Audit', 'Constitutional', 'Statutory', 'All'], 'correct': 3},
        {'text': 'Chief Election Commissioner term = ?', 'options': ['4 years', '5 years', '6 years', '7 years'], 'correct': 1},
        {'text': 'Constitutional amendments need', 'options': ['Simple majority', 'Special majority', 'Unanimous', '2/3 + State'], 'correct': 3},
        {'text': 'Right to property is', 'options': ['Fundamental', 'Constitutional', 'Statutory', 'Moral'], 'correct': 1},
        {'text': 'Fundamental duties are in which Article?', 'options': ['Article 51', 'Article 51A', 'Article 52', 'Article 61'], 'correct': 1},
        {'text': 'Emergency declared under?', 'options': ['Article 352', 'Article 356', 'Article 360', 'All'], 'correct': 3},
        {'text': 'State Emergency by?', 'options': ['Article 352', 'Article 356', 'Article 360', 'None'], 'correct': 1},
        {'text': 'Financial Emergency declared by?', 'options': ['President', 'Parliament', 'Cabinet', 'RBI'], 'correct': 0},
        {'text': 'President appoints Governor on?', 'options': ['Own', 'PM advice', 'CM advice', 'Council'], 'correct': 1},
        {'text': 'Governor can be removed by?', 'options': ['President', 'State', 'Parliament', 'President only'], 'correct': 0},
        {'text': 'National Emergency can last maximum?', 'options': ['1 year', '3 months', 'Unlimited', '6 months'], 'correct': 2},
        {'text': 'Acts passed during emergency need?', 'options': ['No approval', 'Presidential assent', 'Parliamentary approval', 'Judicial review'], 'correct': 1},
    ]
    add_questions(conn, test_id, upsc_gs2)
    
    # ═══════════════════════════════════════════════════════════════════
    # BOARD EXAMS
    # ═══════════════════════════════════════════════════════════════════
    
    # Class 10 Science
    test_id = insert_test(
        'Class 10 Science', 'CBSE Board exam preparation', 
        'Science', 'Board Exam', 30, 60, 'Easy'
    )
    if test_id:
        tests_info.append(('Class 10 Science', test_id))
    
    class10_sci = [
        {'text': 'pH scale ranges from?', 'options': ['0 to 14', '1 to 14', '-7 to 7', '0 to 7'], 'correct': 0},
        {'text': 'Neutral solution has pH = ?', 'options': ['0', '7', '14', '3.5'], 'correct': 1},
        {'text': 'Acid + Base produces?', 'options': ['Salt + Water', 'Salt', 'Water', 'Gas'], 'correct': 0},
        {'text': 'Chemical formula of salt = ?', 'options': ['NaCl', 'H2O', 'HCl', 'O2'], 'correct': 0},
        {'text': 'Valency of oxygen = ?', 'options': ['1', '2', '3', '4'], 'correct': 1},
        {'text': 'Law of conservation of mass by?', 'options': ['Newton', 'Lavoisier', 'Dalton', 'Mendel'], 'correct': 1},
        {'text': 'Mole concept introduced by?', 'options': ['Avogadro', 'Dalton', 'Bohr', 'Faraday'], 'correct': 0},
        {'text': 'Metals conduct electricity because of?', 'options': ['Free electrons', 'Free ions', 'Free atoms', 'Atoms bonded'], 'correct': 0},
        {'text': 'Non-metals are mostly?', 'options': ['Solids', 'Liquids', 'Gases or solids', 'Gases'], 'correct': 2},
        {'text': 'Rusting is?', 'options': ['Physical change', 'Chemical change', 'Both', 'Neither'], 'correct': 1},
        {'text': 'Carbon forms 4 bonds due to?', 'options': ['Electron deficit', 'Electron excess', 'Tetravalent', 'Covalent nature'], 'correct': 2},
        {'text': 'Diamond and Graphite are?', 'options': ['Isomers', 'Allotropes', 'Isotopes', 'Isobars'], 'correct': 1},
        {'text': 'Combustion requires', 'options': ['Fuel', 'Oxygen', 'Heat', 'All'], 'correct': 3},
        {'text': 'Reduction means', 'options': ['Gain of electrons', 'Loss of electrons', 'Gain of oxygen', 'Loss of oxygen'], 'correct': 3},
        {'text': 'Oxidation means', 'options': ['Gain of electrons', 'Loss of electrons', 'Gain of oxygen', 'Loss of hydrogen'], 'correct': 3},
        {'text': 'Redox reaction involves', 'options': ['Only oxidation', 'Only reduction', 'Both', 'Neither'], 'correct': 2},
        {'text': 'Balancing equation uses?', 'options': ['Coefficient only', 'Subscripts', 'Both', 'Charge'], 'correct': 2},
        {'text': 'Lime water turns turbid with?', 'options': ['O2', 'N2', 'CO2', 'H2'], 'correct': 2},
        {'text': 'Most reactive metal = ?', 'options': ['Sodium', 'Potassium', 'Lithium', 'Calcium'], 'correct': 1},
        {'text': 'Least reactive metal = ?', 'options': ['Gold', 'Silver', 'Platinum', 'Copper'], 'correct': 0},
        {'text': 'Displacement reaction shows', 'options': ['Reactivity order', 'Bonds', 'Arrangement', 'Formula'], 'correct': 0},
        {'text': 'Salt formation from acid-base called?', 'options': ['Oxidation', 'Reduction', 'Neutralization', 'Substitution'], 'correct': 2},
        {'text': 'Double displacement produces', 'options': ['New acid', 'New base', 'Precipitate/gas/water', 'Energy'], 'correct': 2},
        {'text': 'Decomposition is reverse of?', 'options': ['Synthesis', 'Displacement', 'Combination', 'Combustion'], 'correct': 0},
        {'text': 'Thermal decomposition of CaCO3 produces?', 'options': ['CaO', 'CO2', 'Both', 'Ca + CO2'], 'correct': 2},
        {'text': 'Electrolysis requires', 'options': ['AC current', 'DC current', 'Both', 'Heat only'], 'correct': 1},
        {'text': 'Anode in electrolysis is?', 'options': ['Positive', 'Negative', 'Neutral', 'Ground'], 'correct': 0},
        {'text': 'Cathode in electrolysis is?', 'options': ['Positive', 'Negative', 'Neutral', 'Ground'], 'correct': 1},
        {'text': 'Cation moves to?', 'options': ['Anode', 'Cathode', 'Both', 'Neither'], 'correct': 1},
        {'text': 'Anion moves to?', 'options': ['Anode', 'Cathode', 'Both', 'Neither'], 'correct': 0},
    ]
    add_questions(conn, test_id, class10_sci)
    
    # Class 12 Physics
    test_id = insert_test(
        'Class 12 Physics', 'CBSE Board exam preparation', 
        'Physics', 'Board Exam', 30, 60, 'Medium'
    )
    if test_id:
        tests_info.append(('Class 12 Physics', test_id))
    
    class12_phys = [
        {'text': 'Electric field lines come from?', 'options': ['Negative charge', 'Positive charge', 'Both', 'Neutrons'], 'correct': 1},
        {'text': 'Capacitor stores?', 'options': ['Current', 'Resistance', 'Charge', 'Voltage'], 'correct': 2},
        {'text': 'Ohm\'s law V = ?', 'options': ['I/R', 'IR', 'R/I', 'I+R'], 'correct': 1},
        {'text': 'Conductivity is inverse of?', 'options': ['Voltage', 'Current', 'Resistance', 'Power'], 'correct': 2},
        {'text': 'Magnetic moment = ?', 'options': ['qvB', 'IA', 'qvr', 'mv'], 'correct': 1},
        {'text': 'Transformer works on?', 'options': ['DC', 'AC', 'Both', 'Neither'], 'correct': 1},
        {'text': 'Photoelectric effect discovered by?', 'options': ['Planck', 'Einstein', 'Bohr', 'Rutherford'], 'correct': 1},
        {'text': 'Planck constant h = ?', 'options': ['6.63×10^-34 Js', '3×10^8', '9.1×10^-31', '1.6×10^-19'], 'correct': 0},
        {'text': 'Bohr model applies to?', 'options': ['Multi-electron atoms', 'Hydrogen only', 'Diatomic molecules', 'Metals'], 'correct': 1},
        {'text': 'Nucleus contains?', 'options': ['Electrons', 'Protons and neutrons', 'Photons', 'Muons'], 'correct': 1},
        {'text': 'Rutherford scattering showed?', 'options': ['Electrons', 'Nucleus', 'Photons', 'Neutrons'], 'correct': 1},
        {'text': 'Alpha particle is?', 'options': ['Electron', 'Proton', 'Helium nucleus', 'Neutron'], 'correct': 2},
        {'text': 'Beta particle is?', 'options': ['Electron', 'Proton', 'Neutron', 'Photon'], 'correct': 0},
        {'text': 'Gamma radiation is?', 'options': ['Particle', 'Electromagnetic', 'Acoustic', 'Particle beam'], 'correct': 1},
        {'text': 'Half-life is', 'options': ['Time to decay half atoms', 'Time to decay nucleus', 'Full decay time', 'Average life'], 'correct': 0},
        {'text': 'Mass-energy relation E = ?', 'options': ['mc', 'mc²', 'm²c', 'mc/2'], 'correct': 1},
        {'text': 'Binding energy is', 'options': ['Positive', 'Negative', 'Zero', 'Variable'], 'correct': 0},
        {'text': 'Nuclear reaction needs?', 'options': ['Heat', 'High energy', 'Catalyst', 'Light'], 'correct': 1},
        {'text': 'Fission splits', 'options': ['Nucleus', 'Electron', 'Atom', 'Molecule'], 'correct': 0},
        {'text': 'Fusion combines', 'options': ['Nucleus', 'Electron', 'Atom', 'Molecules'], 'correct': 0},
        {'text': 'De-Broglie wavelength λ = ?', 'options': ['h/p', 'hp', 'p/h', 'h + p'], 'correct': 0},
        {'text': 'Uncertainty principle states?', 'options': ['Δx·Δp ≥ h/2π', 'Δx·Δp ≤ h', 'Δx = Δp', 'Δx + Δp = h'], 'correct': 0},
        {'text': 'Quantum tunneling is?', 'options': ['Classical', 'Forbidden classically', 'Always happens', 'Impossible'], 'correct': 1},
        {'text': 'Wave function ψ represents?', 'options': ['Probability amplitude', 'Wave', 'Energy', 'Momentum'], 'correct': 0},
        {'text': '|ψ|² represents?', 'options': ['Energy', 'Probability density', 'Amplitude', 'Frequency'], 'correct': 1},
        {'text': 'Superposition principle in quantum says', 'options': ['One state only', 'Multiple states', 'No states', 'States forbidden'], 'correct': 1},
        {'text': 'Entanglement means particles are', 'options': ['Independent', 'Dependent', 'Separated', 'Random'], 'correct': 1},
        {'text': 'Quantum computing uses', 'options': ['Bits', 'Qubits', 'Both', 'Superposition'], 'correct': 1},
        {'text': 'Quantum cryptography ensures', 'options': ['Speed', 'Security', 'Compression', 'Simplicity'], 'correct': 1},
        {'text': 'Bell\'s theorem shows', 'options': ['Local realism', 'Quantum nature', 'Classical physics', 'Determinism'], 'correct': 1},
    ]
    add_questions(conn, test_id, class12_phys)
    
    # ═══════════════════════════════════════════════════════════════════
    # COMPETITIVE EXAMS
    # ═══════════════════════════════════════════════════════════════════
    
    # CAT - Quantitative Aptitude
    test_id = insert_test(
        'CAT - Quantitative Aptitude', 'MBA entrance exam', 
        'Quantitative Aptitude', 'CAT', 30, 60, 'Hard'
    )
    if test_id:
        tests_info.append(('CAT - Quantitative', test_id))
    
    cat_quant = [
        {'text': 'If x² + y² = 34 and xy = 15, then x + y = ?', 'options': ['8', '±8', '4', '±4'], 'correct': 1},
        {'text': 'Simple interest on 1000 at 5% for 2 years = ?', 'options': ['50', '100', '105', '110'], 'correct': 1},
        {'text': 'If cost price is 100 and profit is 25%, selling price = ?', 'options': ['100', '125', '120', '150'], 'correct': 1},
        {'text': 'Average of 5, 10, 15, 20, 25 = ?', 'options': ['13', '15', '17', '19'], 'correct': 1},
        {'text': 'In ratio 3:4:5, if sum = 60, smallest part = ?', 'options': ['12', '15', '18', '20'], 'correct': 0},
        {'text': 'LCM of 12 and 18 = ?', 'options': ['36', '24', '18', '6'], 'correct': 0},
        {'text': 'Percentage change from 50 to 75 = ?', 'options': ['25%', '30%', '50%', '33.33%'], 'correct': 2},
        {'text': 'If A:B = 2:3 and B:C = 4:5, then A:B:C = ?', 'options': ['2:3:4', '8:12:15', '2:4:5', '1:1.5:1.87'], 'correct': 1},
        {'text': 'Time taken to cover 100km at 50km/hr = ?', 'options': ['2 hrs', '1 hr', '3 hrs', '1.5 hrs'], 'correct': 0},
        {'text': 'If a=2, b=3, find 2a²+3b² = ?', 'options': ['35', '40', '43', '50'], 'correct': 2},
        {'text': 'Compound interest for 2 years at 10% on 100?', 'options': ['20', '21', '22', '23'], 'correct': 1},
        {'text': 'If price increases 10% then decreases 10%, net change?', 'options': ['0%', '-1%', '+1%', '-2%'], 'correct': 1},
        {'text': 'A works in 5 days, B works in 6 days. Together?', 'options': ['30/11', '11/30', '6/5', '5/6'], 'correct': 0},
        {'text': 'Two numbers in ratio 3:4, sum = 105, numbers?', 'options': ['45, 60', '30, 75', '35, 70', '40, 65'], 'correct': 0},
        {'text': 'Speed = ?', 'options': ['Distance × Time', 'Distance / Time', 'Time / Distance', 'Distance + Time'], 'correct': 1},
        {'text': 'Area of triangle = ?', 'options': ['1/2 × base × height', 'base × height', '2 × base × height', 'base + height'], 'correct': 0},
        {'text': 'Circumference of circle = ?', 'options': ['πr', '2πr', 'πr²', '2πr²'], 'correct': 1},
        {'text': 'Volume of cube = ?', 'options': ['a²', 'a³', '6a²', '3a'], 'correct': 1},
        {'text': 'Surface area of sphere = ?', 'options': ['4πr²', '2πr²', 'πr²', '3πr²'], 'correct': 0},
        {'text': 'Volume of sphere = ?', 'options': ['4πr³', '4/3 πr³', '3/4 πr³', '2πr³'], 'correct': 1},
        {'text': 'Quadratic mean > Arithmetic mean > Geometric mean > Harmonic mean for?', 'options': ['Equal numbers', 'Unequal positive', 'Negative', 'Zero'], 'correct': 1},
        {'text': 'Mode is', 'options': ['Middle value', 'Average', 'Most frequent', 'Spread'], 'correct': 2},
        {'text': 'Variance is', 'options': ['Range', 'Mean', 'Average of squared deviations', 'Median'], 'correct': 2},
        {'text': 'Standard deviation unit is', 'options': ['None', 'Square of original', 'Same as original', 'Percentage'], 'correct': 2},
        {'text': 'Correlation coefficient ranges', 'options': ['-1 to 1', '0 to 1', '-∞ to ∞', '0 to ∞'], 'correct': 0},
        {'text': 'Probability of an event ranges', 'options': ['-1 to 1', '0 to 1', '0 to 2', '-∞ to ∞'], 'correct': 1},
        {'text': 'If P(A) = 0.3, then P(A\') = ?', 'options': ['0.3', '0.7', '0', '1'], 'correct': 1},
        {'text': 'Permutation P(n,r) = ?', 'options': ['n!/(n-r)!', 'n!/r!(n-r)!', 'n^r', 'r^n'], 'correct': 0},
        {'text': 'Combination C(n,r) = ?', 'options': ['n!/(n-r)!', 'n!/r!(n-r)!', 'n^r', 'r!/(n-r)!'], 'correct': 1},
        {'text': 'Sum of arithmetic series = ?', 'options': ['n/2(a+l)', 'n(a+l)', 'a+l/2', 'n(a+l)/2'], 'correct': 0},
    ]
    add_questions(conn, test_id, cat_quant)
    
    # GMAT - Verbal
    test_id = insert_test(
        'GMAT - Verbal Reasoning', 'Graduate management entrance exam', 
        'Verbal Reasoning', 'GMAT', 30, 65, 'Hard'
    )
    if test_id:
        tests_info.append(('GMAT - Verbal', test_id))
    
    gmat_verbal = [
        {'text': 'Choose the grammatically correct sentence', 'options': ['He don\'t go there', 'He doesn\'t go there', 'He not go there', 'He gone not'], 'correct': 1},
        {'text': 'Synonym of "perspicacious" = ?', 'options': ['Lazy', 'Shrewd', 'Loud', 'Boring'], 'correct': 1},
        {'text': 'Antonym of "benevolent" = ?', 'options': ['Kind', 'Malevolent', 'Generous', 'Noble'], 'correct': 1},
        {'text': 'Fill blank: "She _____ to the office every day"', 'options': ['go', 'goes', 'going', 'gone'], 'correct': 1},
        {'text': 'Which is a complex sentence?', 'options': ['I like cats', 'I like cats and dogs', 'I like cats because they are cute', 'Cats are cute'], 'correct': 2},
        {'text': 'Choose correct pronoun: "Him and _____ are friends"', 'options': ['me', 'I', 'myself', 'mine'], 'correct': 1},
        {'text': 'Plural of "crisis" = ?', 'options': ['crises', 'crisises', 'crisis', 'crisisess'], 'correct': 0},
        {'text': 'Choose best phrase: "As per _____ information"', 'options': ['your', 'you\'re', 'yours', 'yu\'r'], 'correct': 0},
        {'text': 'Correct form: "If I were rich, I _____ travel"', 'options': ['will', 'would', 'shall', 'am'], 'correct': 1},
        {'text': 'What is active voice of "The cake was eaten by her"?', 'options': ['She eats the cake', 'She ate the cake', 'She is eating cake', 'She have eaten cake'], 'correct': 1},
        {'text': 'Parallel structure means', 'options': ['Same grammar', 'Same tense', 'Same construction', 'All'], 'correct': 3},
        {'text': 'Dangling modifier is', 'options': ['Correct', 'Unclear reference', 'Repeated word', 'Long phrase'], 'correct': 1},
        {'text': 'Subject-verb agreement requires', 'options': ['Same number', 'Same tense', 'Same case', 'Same gender'], 'correct': 0},
        {'text': 'Fragment is', 'options': ['Complete sentence', 'Incomplete sentence', 'Long phrase', 'Question'], 'correct': 1},
        {'text': 'Run-on sentence has', 'options': ['One clause', 'Independent clauses without conjunction', 'Many words', 'Repetition'], 'correct': 1},
        {'text': 'Apostrophe shows', 'options': ['Pause', 'Possession or contraction', 'Emphasis', 'Question'], 'correct': 1},
        {'text': 'Comma splice is joining clauses with', 'options': ['Period', 'Semicolon', 'Comma', 'Dash'], 'correct': 2},
        {'text': 'Semicolon joins', 'options': ['Any clauses', 'Independent clauses', 'Dependent clauses', 'Phrases'], 'correct': 1},
        {'text': 'Colon introduces', 'options': ['Question', 'List or explanation', 'Contrast', 'Reason'], 'correct': 1},
        {'text': 'Hyphenate compound when it', 'options': ['Is adjective', 'Precedes noun', 'Comes after noun', 'Both A and B'], 'correct': 3},
        {'text': 'Affect vs Effect - Affect is', 'options': ['Noun', 'Verb', 'Adjective', 'Adverb'], 'correct': 1},
        {'text': 'Its vs It\'s - Its is', 'options': ['Possession', 'It is', 'Plural', 'Adverb'], 'correct': 0},
        {'text': 'Your vs You\'re - You\'re is', 'options': ['Possession', 'You are', 'Plural', 'Adjective'], 'correct': 1},
        {'text': 'Their vs There - Their shows', 'options': ['Location', 'Possession', 'Plural', 'Adverb'], 'correct': 1},
        {'text': 'Where vs Were - Were is', 'options': ['Location', 'Past tense of be', 'Question', 'Adverb'], 'correct': 1},
        {'text': 'Accept vs Except - Accept means', 'options': ['Exclude', 'Receive', 'Except', 'Exclude'], 'correct': 1},
        {'text': 'Principle vs Principal - Principle is', 'options': ['School head', 'Rule', 'Money', 'First'], 'correct': 1},
        {'text': 'Advice vs Advise - Advice is', 'options': ['Noun', 'Verb', 'Adjective', 'Adverb'], 'correct': 0},
        {'text': 'Weather vs Whether - Whether shows', 'options': ['Climate', 'Choice', 'Atmosphere', 'Condition'], 'correct': 1},
        {'text': 'Waist vs Waste - Waist is', 'options': ['Garbage', 'Body part', 'Spend', 'Trash'], 'correct': 1},
    ]
    add_questions(conn, test_id, gmat_verbal)
    
    conn.commit()
    conn.close()
    
    print("✅ Comprehensive mock tests populated successfully!")
    print(f"\n📚 Total Tests Created: {len(tests_info)}")
    for name, tid in tests_info:
        print(f"   ✓ {name} (ID: {tid})")
    print("\n🚀 Access mock tests at: http://localhost:5000/mocktest")

if __name__ == '__main__':
    populate_sample_tests()
