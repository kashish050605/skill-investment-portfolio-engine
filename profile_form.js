let selectedSkills = [];
let currentStep = 1;

function goToStep2() {
  const name = document.getElementById('name').value.trim();
  const exp = document.querySelector('input[name="exp"]:checked');
  const err = document.getElementById('err1');
  if (!name) { err.textContent = 'Please enter your name.'; return; }
  if (!exp)  { err.textContent = 'Please select your experience level.'; return; }
  err.textContent = '';
  showStep(2);
}

function goToStep1() { showStep(1); }

function goToStep3() {
  const err = document.getElementById('err2');
  if (selectedSkills.length === 0) { err.textContent = 'Please select at least one skill.'; return; }
  err.textContent = '';
  showStep(3);
  runEngine();
}

function showStep(n) {
  currentStep = n;
  document.querySelectorAll('.form-step').forEach(s => s.classList.add('hidden'));
  document.getElementById('formStep' + n).classList.remove('hidden');
  updateStepDots(n);
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function updateStepDots(n) {
  for (let i = 1; i <= 3; i++) {
    const dot = document.getElementById('step' + i + '-dot');
    dot.classList.remove('active', 'done');
    if (i < n)  dot.classList.add('done');
    if (i === n) dot.classList.add('active');
  }
  document.querySelectorAll('.step-line').forEach((line, idx) => {
    line.classList.toggle('done', idx + 1 < n);
  });
}

function toggleSkill(el) {
  el.classList.toggle('selected');
  const skill = el.dataset.skill;
  if (el.classList.contains('selected')) {
    if (!selectedSkills.includes(skill)) selectedSkills.push(skill);
  } else {
    selectedSkills = selectedSkills.filter(s => s !== skill);
  }
  const cnt = document.getElementById('selectedCount');
  cnt.textContent = selectedSkills.length + ' skill' + (selectedSkills.length !== 1 ? 's' : '') + ' selected';
}

function runEngine() {
  const name = document.getElementById('name').value.trim();
  const exp  = document.querySelector('input[name="exp"]:checked').value;

  const userProfile = { name, experience: exp, skills: selectedSkills };

  const marketData = window.marketData || {
    Python: 'High', SQL: 'High', Excel: 'Medium',
    'Power BI': 'Medium', 'Machine Learning': 'High',
    Blockchain: 'Low', JavaScript: 'High',
    'Cloud (AWS/GCP)': 'High', 'Data Science': 'High'
  };

  window.userProfile = userProfile;
  window.marketData  = marketData;
  console.log('[SkillPort] userProfile:', JSON.stringify(userProfile, null, 2));

  if (typeof allocateSkills === 'function') {
    try {
      const result = allocateSkills(userProfile, marketData);
      document.getElementById('loadingState').style.display = 'none';
      document.getElementById('resultSubtitle').textContent = 'Here\'s your personalised skill portfolio, ' + name + '.';
      sendToOutput(result);
    } catch (err) {
      showFallback(name, exp);
      console.error('allocateSkills error:', err);
    }
  } else {
    setTimeout(() => showFallback(name, exp), 1400);
  }
}

function sendToOutput(result) {
  const el = document.getElementById('outputContent');
  el.style.display = 'block';
  if (typeof renderOutput === 'function') {
    renderOutput(result, el);
  } else {
    el.innerHTML = `<div style="background:rgba(79,255,176,0.08);border:1px solid rgba(79,255,176,0.2);border-radius:10px;padding:1.2rem;font-size:0.85rem;color:#4fffb0;margin-top:1rem;"><strong>Engine result received!</strong><pre style="margin-top:8px;white-space:pre-wrap;color:#a0ffd8;">${JSON.stringify(result, null, 2)}</pre></div>`;
  }
}

function showFallback(name, exp) {
  document.getElementById('loadingState').style.display = 'none';
  document.getElementById('resultSubtitle').textContent = 'Profile ready! Waiting for AI engine to connect.';
  document.getElementById('sumName').textContent   = name;
  document.getElementById('sumExp').textContent    = exp.charAt(0).toUpperCase() + exp.slice(1);
  document.getElementById('sumSkills').textContent = selectedSkills.join(', ');
  document.getElementById('profileSummary').style.display = 'block';
}

function resetAll() {
  document.getElementById('name').value = '';
  document.querySelectorAll('input[name="exp"]').forEach(r => r.checked = false);
  document.querySelectorAll('.skill-tile').forEach(t => t.classList.remove('selected'));
  document.getElementById('selectedCount').textContent = '0 skills selected';
  document.getElementById('outputContent').style.display = 'none';
  document.getElementById('outputContent').innerHTML = '';
  document.getElementById('profileSummary').style.display = 'none';
  document.getElementById('loadingState').style.display = 'flex';
  selectedSkills = [];
  showStep(1);
}