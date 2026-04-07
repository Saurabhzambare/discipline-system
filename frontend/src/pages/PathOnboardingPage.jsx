import { useEffect, useMemo, useState } from 'react';
import {
  completeOnboarding,
  getAlchemistSetupGuide,
  getOnboardingStatus,
  saveDisciplineKnightOnboarding,
  saveFitnessWarriorOnboarding,
  saveGrindVisionaryOnboarding,
  saveHealthAlchemistOnboarding,
  saveMindsetSageOnboarding,
  submitDisciplineCode,
} from '../api';

const CARD = 'rounded-2xl border border-[#1a3a5c] bg-[#0a1628] p-5';

function OptionGrid({ options, value, onChange }) {
  return (
    <div className="grid gap-2 sm:grid-cols-2">
      {options.map((option) => (
        <button
          key={option.value}
          type="button"
          onClick={() => onChange(option.value)}
          className={`rounded-lg border px-3 py-2 text-left text-sm ${
            value === option.value
              ? 'border-cyan-400/70 bg-cyan-500/15 text-cyan-100'
              : 'border-[#1a3a5c] bg-[#071020] text-slate-300'
          }`}
        >
          {option.label}
        </button>
      ))}
    </div>
  );
}

function FitnessForm({ onSubmit }) {
  const [form, setForm] = useState({
    training_split: 'ppl',
    primary_goal: 'general_performance',
    training_days_per_week: 4,
    experience_level: 'beginner',
    split_day_start: 'push',
  });

  const needsSplitStart = form.training_split === 'ppl' || form.training_split === 'bro_split';

  return (
    <div className={CARD}>
      <h2 className="mb-3 text-lg font-bold text-slate-100">Fitness Warrior Onboarding</h2>
      <p className="mb-4 text-sm text-slate-400">Build your training profile.</p>
      <div className="space-y-4">
        <div>
          <p className="mb-2 text-xs uppercase tracking-wide text-slate-500">Training Split</p>
          <OptionGrid
            value={form.training_split}
            onChange={(v) => setForm((p) => ({ ...p, training_split: v }))}
            options={[
              { value: 'ppl', label: 'PPL' },
              { value: 'full_body', label: 'Full Body' },
              { value: 'bro_split', label: 'Bro Split' },
              { value: 'calisthenics', label: 'Calisthenics' },
              { value: 'cardio_focused', label: 'Cardio Focused' },
              { value: 'custom', label: 'Custom' },
            ]}
          />
        </div>

        <div>
          <p className="mb-2 text-xs uppercase tracking-wide text-slate-500">Primary Goal</p>
          <OptionGrid
            value={form.primary_goal}
            onChange={(v) => setForm((p) => ({ ...p, primary_goal: v }))}
            options={[
              { value: 'muscle_gain', label: 'Muscle Gain' },
              { value: 'fat_loss', label: 'Fat Loss' },
              { value: 'recomp', label: 'Recomp' },
              { value: 'general_performance', label: 'General Performance' },
            ]}
          />
        </div>

        <div>
          <p className="mb-2 text-xs uppercase tracking-wide text-slate-500">Training Days Per Week</p>
          <OptionGrid
            value={form.training_days_per_week}
            onChange={(v) => setForm((p) => ({ ...p, training_days_per_week: v }))}
            options={[3, 4, 5, 6, 7].map((d) => ({ value: d, label: `${d} days` }))}
          />
        </div>

        <div>
          <p className="mb-2 text-xs uppercase tracking-wide text-slate-500">Experience Level</p>
          <OptionGrid
            value={form.experience_level}
            onChange={(v) => setForm((p) => ({ ...p, experience_level: v }))}
            options={[
              { value: 'beginner', label: 'Beginner' },
              { value: 'intermediate', label: 'Intermediate' },
              { value: 'advanced', label: 'Advanced' },
            ]}
          />
        </div>

        {needsSplitStart && (
          <div>
            <p className="mb-2 text-xs uppercase tracking-wide text-slate-500">Split Day Start</p>
            <OptionGrid
              value={form.split_day_start}
              onChange={(v) => setForm((p) => ({ ...p, split_day_start: v }))}
              options={[
                { value: 'push', label: 'Push Day' },
                { value: 'pull', label: 'Pull Day' },
                { value: 'legs', label: 'Leg Day' },
                { value: 'rest', label: 'Rest Day' },
                { value: 'fresh_start', label: 'Starting Fresh' },
              ]}
            />
          </div>
        )}

        <button type="button" onClick={() => onSubmit(form)} className="rounded-lg border border-cyan-500/50 bg-cyan-500/10 px-4 py-2 text-cyan-200">
          Save Fitness Setup
        </button>
      </div>
    </div>
  );
}

function MindsetForm({ onSubmit }) {
  const [form, setForm] = useState({
    motivation: 'personal_growth',
    daily_time_commitment: '30_minutes',
    experience_level: 'complete_beginner',
    archetype: 'warrior_sage',
  });

  return (
    <div className={CARD}>
      <h2 className="mb-3 text-lg font-bold text-slate-100">Mindset Sage Onboarding</h2>
      <div className="space-y-4">
        <OptionGrid
          value={form.motivation}
          onChange={(v) => setForm((p) => ({ ...p, motivation: v }))}
          options={[
            { value: 'mental_clarity', label: 'Mental Clarity' },
            { value: 'stress_relief', label: 'Stress Relief' },
            { value: 'personal_growth', label: 'Personal Growth' },
            { value: 'discipline_building', label: 'Discipline Building' },
          ]}
        />
        <OptionGrid
          value={form.daily_time_commitment}
          onChange={(v) => setForm((p) => ({ ...p, daily_time_commitment: v }))}
          options={[
            { value: '15_minutes', label: '15 minutes' },
            { value: '30_minutes', label: '30 minutes' },
            { value: '1_hour', label: '1 hour' },
            { value: 'as_much_as_needed', label: 'As much as needed' },
          ]}
        />
        <OptionGrid
          value={form.experience_level}
          onChange={(v) => setForm((p) => ({ ...p, experience_level: v }))}
          options={[
            { value: 'complete_beginner', label: 'Complete Beginner' },
            { value: 'some_experience', label: 'Some Experience' },
            { value: 'daily_practitioner', label: 'Daily Practitioner' },
          ]}
        />
        <OptionGrid
          value={form.archetype}
          onChange={(v) => setForm((p) => ({ ...p, archetype: v }))}
          options={[
            { value: 'stoic', label: 'The Stoic' },
            { value: 'scholar', label: 'The Scholar' },
            { value: 'monk', label: 'The Monk' },
            { value: 'warrior_sage', label: 'The Warrior-Sage' },
          ]}
        />

        <button type="button" onClick={() => onSubmit(form)} className="rounded-lg border border-cyan-500/50 bg-cyan-500/10 px-4 py-2 text-cyan-200">
          Save Mindset Setup
        </button>
      </div>
    </div>
  );
}

function HealthForm({ onSubmit, setupGuide, onLoadGuide }) {
  const [form, setForm] = useState({
    primary_health_goal: 'full_body_transformation',
    health_relationship: 'starting_from_scratch',
    focus_area: 'all_of_them',
    equipment_list: [],
  });

  const equipmentOptions = [
    ['cold_shower', 'Cold Shower'],
    ['cold_plunge', 'Ice Bath / Cold Plunge'],
    ['sauna', 'Sauna'],
    ['fitness_tracker', 'Fitness Tracker'],
    ['supplements', 'Supplements'],
    ['none_yet', 'None Yet'],
  ];

  const toggleEquipment = (key) => {
    setForm((prev) => ({
      ...prev,
      equipment_list: prev.equipment_list.includes(key)
        ? prev.equipment_list.filter((i) => i !== key)
        : [...prev.equipment_list, key],
    }));
  };

  return (
    <div className="space-y-4">
      <div className={CARD}>
        <h2 className="mb-3 text-lg font-bold text-slate-100">Health Alchemist Onboarding</h2>
        <div className="space-y-4">
          <OptionGrid
            value={form.primary_health_goal}
            onChange={(v) => setForm((p) => ({ ...p, primary_health_goal: v }))}
            options={[
              { value: 'optimize_energy', label: 'Optimize Energy' },
              { value: 'reduce_stress_and_burnout', label: 'Reduce Stress & Burnout' },
              { value: 'improve_gut_health', label: 'Improve Gut Health' },
              { value: 'build_better_sleep', label: 'Build Better Sleep' },
              { value: 'full_body_transformation', label: 'Full Body Transformation' },
            ]}
          />
          <OptionGrid
            value={form.health_relationship}
            onChange={(v) => setForm((p) => ({ ...p, health_relationship: v }))}
            options={[
              { value: 'starting_from_scratch', label: 'Starting From Scratch' },
              { value: 'some_good_habits', label: 'Some Good Habits' },
              { value: 'already_health_conscious', label: 'Already Health Conscious' },
              { value: 'biohack_and_optimize', label: 'Biohack & Optimize' },
            ]}
          />
          <OptionGrid
            value={form.focus_area}
            onChange={(v) => setForm((p) => ({ ...p, focus_area: v }))}
            options={[
              { value: 'nutrition', label: 'Nutrition' },
              { value: 'sleep', label: 'Sleep' },
              { value: 'mental_health', label: 'Mental Health' },
              { value: 'hydration', label: 'Hydration' },
              { value: 'all_of_them', label: 'All Of Them' },
            ]}
          />

          <div>
            <p className="mb-2 text-xs uppercase tracking-wide text-slate-500">Equipment Access (multi-select)</p>
            <div className="grid gap-2 sm:grid-cols-2">
              {equipmentOptions.map(([key, label]) => (
                <button
                  key={key}
                  type="button"
                  onClick={() => toggleEquipment(key)}
                  className={`rounded-lg border px-3 py-2 text-left text-sm ${
                    form.equipment_list.includes(key)
                      ? 'border-cyan-400/70 bg-cyan-500/15 text-cyan-100'
                      : 'border-[#1a3a5c] bg-[#071020] text-slate-300'
                  }`}
                >
                  {label}
                </button>
              ))}
            </div>
          </div>

          <div className="flex gap-2">
            <button type="button" onClick={() => onSubmit(form)} className="rounded-lg border border-cyan-500/50 bg-cyan-500/10 px-4 py-2 text-cyan-200">
              Save Alchemist Setup
            </button>
            <button type="button" onClick={onLoadGuide} className="rounded-lg border border-emerald-500/50 bg-emerald-500/10 px-4 py-2 text-emerald-200">
              Load Setup Guide
            </button>
          </div>
        </div>
      </div>

      {setupGuide ? (
        <div className={CARD}>
          <p className="text-xs text-amber-300 mb-3">{setupGuide.disclaimer_top}</p>
          <h3 className="text-md font-bold text-slate-100 mb-2">Supplement Cards</h3>
          <div className="space-y-2 mb-3">
            {setupGuide.supplements.map((s) => (
              <div key={s.key} className="rounded-lg border border-[#1a3a5c] bg-[#071020] p-3">
                <p className="font-semibold text-slate-200">{s.name}</p>
                <p className="text-xs text-slate-400">Take It: {s.take_it}</p>
                <p className="text-xs text-slate-400">Eat It Instead: {s.eat_it_instead}</p>
                <p className="text-[11px] text-amber-300 mt-1">{s.disclaimer}</p>
              </div>
            ))}
          </div>
          <h3 className="text-md font-bold text-slate-100 mb-2">Equipment Cards</h3>
          <div className="space-y-2">
            {setupGuide.equipment_cards.map((e) => (
              <div key={e.key} className="rounded-lg border border-[#1a3a5c] bg-[#071020] p-3">
                <p className="font-semibold text-slate-200">{e.name}</p>
                <p className="text-xs text-slate-400">Budget alternative: {e.budget_alternative}</p>
              </div>
            ))}
          </div>
          <div className="mt-3 rounded-lg border border-emerald-500/30 bg-emerald-500/10 p-3 text-sm text-emerald-200">
            {setupGuide.starter_pack?.message}
          </div>
          <p className="text-xs text-amber-300 mt-3">{setupGuide.disclaimer_bottom}</p>
        </div>
      ) : null}
    </div>
  );
}

function DisciplineForm({ onSave, onOath, oathError }) {
  const [form, setForm] = useState({
    routine_level: 'no_routine',
    biggest_challenge: 'all_of_them',
    structure_preference: 'semi_structured',
    time_commitment: '1_hour',
  });
  const [rules, setRules] = useState(['', '', '']);

  return (
    <div className={CARD}>
      <h2 className="mb-3 text-lg font-bold text-slate-100">Discipline Knight Onboarding</h2>
      <div className="space-y-3">
        <OptionGrid
          value={form.routine_level}
          onChange={(v) => setForm((p) => ({ ...p, routine_level: v }))}
          options={[
            { value: 'no_routine', label: 'No Routine' },
            { value: 'partial_routine', label: 'Partial Routine' },
            { value: 'routine_but_break_often', label: 'Routine but Break Often' },
            { value: 'solid_routine_level_up', label: 'Solid Routine, Level Up' },
          ]}
        />
        <OptionGrid
          value={form.biggest_challenge}
          onChange={(v) => setForm((p) => ({ ...p, biggest_challenge: v }))}
          options={[
            { value: 'wake_consistently', label: 'Waking Consistently' },
            { value: 'staying_focused', label: 'Staying Focused' },
            { value: 'resisting_distractions', label: 'Resisting Distractions' },
            { value: 'managing_money', label: 'Managing Money' },
            { value: 'all_of_them', label: 'All Of Them' },
          ]}
        />
        <OptionGrid
          value={form.structure_preference}
          onChange={(v) => setForm((p) => ({ ...p, structure_preference: v }))}
          options={[
            { value: 'fully_structured', label: 'Fully Structured' },
            { value: 'semi_structured', label: 'Semi Structured' },
            { value: 'flexible', label: 'Flexible' },
          ]}
        />
        <OptionGrid
          value={form.time_commitment}
          onChange={(v) => setForm((p) => ({ ...p, time_commitment: v }))}
          options={[
            { value: '30_minutes', label: '30 Minutes' },
            { value: '1_hour', label: '1 Hour' },
            { value: '2_hours', label: '2 Hours' },
            { value: 'as_much_as_it_takes', label: 'As Much As It Takes' },
          ]}
        />

        <button type="button" onClick={() => onSave(form)} className="rounded-lg border border-cyan-500/50 bg-cyan-500/10 px-4 py-2 text-cyan-200">
          Save Knight Setup
        </button>

        <div className="rounded-lg border border-[#1a3a5c] bg-[#071020] p-3">
          <p className="text-sm font-semibold text-slate-100 mb-2">Discipline Code Oath (3–5 rules)</p>
          {rules.map((rule, index) => (
            <input
              key={index}
              value={rule}
              onChange={(e) => {
                const next = [...rules];
                next[index] = e.target.value;
                setRules(next);
              }}
              placeholder={`Rule ${index + 1}`}
              className="mb-2 w-full rounded border border-slate-700 bg-slate-900 px-2 py-1 text-sm text-slate-100"
            />
          ))}
          {rules.length < 5 && (
            <button type="button" onClick={() => setRules((r) => [...r, ''])} className="mr-2 text-xs text-cyan-300">+ Add Rule</button>
          )}
          {rules.length > 3 && (
            <button type="button" onClick={() => setRules((r) => r.slice(0, -1))} className="text-xs text-rose-300">- Remove Rule</button>
          )}

          {oathError ? <p className="mt-2 text-xs text-rose-300">{oathError}</p> : null}

          <button
            type="button"
            onClick={() => onOath(rules.filter((r) => r.trim()))}
            className="mt-3 rounded-lg border border-amber-500/50 bg-amber-500/10 px-4 py-2 text-amber-200"
          >
            Submit Oath
          </button>
        </div>
      </div>
    </div>
  );
}

function GrindForm({ onSubmit }) {
  const [form, setForm] = useState({
    grind_focus: 'coding_and_tech',
    grind_focus_other: '',
    experience_state: 'complete_beginner',
    singular_goal_text: '',
    goal_timeline: '1_year',
    daily_hours: '1_hour',
    current_output_state: 'consume_more_than_create',
  });

  return (
    <div className={CARD}>
      <h2 className="mb-3 text-lg font-bold text-slate-100">Grind Visionary Onboarding</h2>
      <div className="space-y-3">
        <OptionGrid
          value={form.grind_focus}
          onChange={(v) => setForm((p) => ({ ...p, grind_focus: v }))}
          options={[
            { value: 'coding_and_tech', label: 'Coding & Tech' },
            { value: 'design_and_creative', label: 'Design & Creative' },
            { value: 'writing_and_content', label: 'Writing & Content' },
            { value: 'business_and_entrepreneurship', label: 'Business' },
            { value: 'marketing_and_growth', label: 'Marketing' },
            { value: 'finance_and_investing', label: 'Finance' },
            { value: 'other', label: 'Other' },
          ]}
        />
        {form.grind_focus === 'other' && (
          <input
            value={form.grind_focus_other}
            onChange={(e) => setForm((p) => ({ ...p, grind_focus_other: e.target.value }))}
            placeholder="Name your field"
            className="w-full rounded border border-slate-700 bg-slate-900 px-2 py-2 text-sm text-slate-100"
          />
        )}

        <OptionGrid
          value={form.experience_state}
          onChange={(v) => setForm((p) => ({ ...p, experience_state: v }))}
          options={[
            { value: 'complete_beginner', label: 'Complete Beginner' },
            { value: 'some_skills_go_deeper', label: 'Some Skills' },
            { value: 'intermediate_ready_to_ship', label: 'Intermediate' },
            { value: 'advanced_scaling', label: 'Advanced' },
          ]}
        />

        <input
          value={form.singular_goal_text}
          onChange={(e) => setForm((p) => ({ ...p, singular_goal_text: e.target.value }))}
          placeholder="In 12 months I want to..."
          className="w-full rounded border border-slate-700 bg-slate-900 px-2 py-2 text-sm text-slate-100"
        />

        <OptionGrid
          value={form.goal_timeline}
          onChange={(v) => setForm((p) => ({ ...p, goal_timeline: v }))}
          options={[
            { value: '3_months', label: '3 Months' },
            { value: '6_months', label: '6 Months' },
            { value: '1_year', label: '1 Year' },
            { value: '2_years', label: '2 Years' },
          ]}
        />

        <OptionGrid
          value={form.daily_hours}
          onChange={(v) => setForm((p) => ({ ...p, daily_hours: v }))}
          options={[
            { value: '30_minutes', label: '30 Minutes' },
            { value: '1_hour', label: '1 Hour' },
            { value: '2_hours', label: '2 Hours' },
            { value: '3_plus_hours', label: '3+ Hours' },
          ]}
        />

        <OptionGrid
          value={form.current_output_state}
          onChange={(v) => setForm((p) => ({ ...p, current_output_state: v }))}
          options={[
            { value: 'consume_more_than_create', label: 'Consume > Create' },
            { value: 'create_occasionally', label: 'Create Occasionally' },
            { value: 'ship_regularly', label: 'Ship Regularly' },
            { value: 'audience_or_income_already', label: 'Audience/Income Already' },
          ]}
        />

        <button type="button" onClick={() => onSubmit(form)} className="rounded-lg border border-cyan-500/50 bg-cyan-500/10 px-4 py-2 text-cyan-200">
          Save Visionary Setup
        </button>
      </div>
    </div>
  );
}

export default function PathOnboardingPage({ player, onNavigate, onOnboardingComplete }) {
  const [status, setStatus] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);
  const [setupGuide, setSetupGuide] = useState(null);
  const [oathError, setOathError] = useState('');

  const path = player?.path || '';

  useEffect(() => {
    async function load() {
      try {
        setLoading(true);
        const data = await getOnboardingStatus();
        setStatus(data);
      } catch (err) {
        setError(err.message || 'Could not load onboarding status.');
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  const finish = async () => {
    setError('');
    const pathCode = status?.path_code || path;

    if (!pathCode) {
      setError('Could not determine your selected path for onboarding completion.');
      return;
    }

    try {
      const response = await completeOnboarding(pathCode);
      if (onOnboardingComplete) onOnboardingComplete(response.player);
      onNavigate('/dashboard');
    } catch (err) {
      setError(err.message || 'Could not complete onboarding.');
    }
  };

  const actions = useMemo(() => ({
    fitness_warrior: (payload) => saveFitnessWarriorOnboarding(payload),
    mindset_sage: (payload) => saveMindsetSageOnboarding(payload),
    health_alchemist: (payload) => saveHealthAlchemistOnboarding(payload),
    discipline_knight: (payload) => saveDisciplineKnightOnboarding(payload),
    grind_visionary: (payload) => saveGrindVisionaryOnboarding(payload),
  }), []);

  const handleSave = async (payload) => {
    setError('');
    try {
      await actions[path](payload);
      const refreshed = await getOnboardingStatus();
      setStatus(refreshed);
    } catch (err) {
      setError(err.message || 'Could not save onboarding data.');
    }
  };

  const handleOath = async (rules) => {
    setOathError('');
    try {
      await submitDisciplineCode(rules);
      const refreshed = await getOnboardingStatus();
      setStatus(refreshed);
    } catch (err) {
      setOathError(err.message || 'Could not save discipline code.');
    }
  };

  const handleLoadGuide = async () => {
    setError('');
    try {
      const guide = await getAlchemistSetupGuide();
      setSetupGuide(guide);
    } catch (err) {
      setError(err.message || 'Could not load setup guide.');
    }
  };

  if (loading) {
    return <div className="p-8 text-slate-400">Loading onboarding...</div>;
  }

  return (
    <div className="min-h-screen bg-[#050d1a] p-4 sm:p-8">
      <div className="mx-auto max-w-3xl space-y-4">
        <div className={CARD}>
          <p className="text-xs uppercase tracking-[0.3em] text-cyan-400/70">Path Onboarding</p>
          <h1 className="mt-1 text-2xl font-black text-slate-100">Complete your setup</h1>
          <p className="mt-2 text-sm text-slate-400">
            Resume-safe status: <span className="text-cyan-300">{status?.current_step || 'start'}</span>
          </p>
          {error ? <p className="mt-2 text-sm text-rose-300">{error}</p> : null}
        </div>

        {path === 'fitness_warrior' && <FitnessForm onSubmit={handleSave} />}
        {path === 'mindset_sage' && <MindsetForm onSubmit={handleSave} />}
        {path === 'health_alchemist' && (
          <HealthForm onSubmit={handleSave} setupGuide={setupGuide} onLoadGuide={handleLoadGuide} />
        )}
        {path === 'discipline_knight' && (
          <DisciplineForm onSave={handleSave} onOath={handleOath} oathError={oathError} />
        )}
        {path === 'grind_visionary' && <GrindForm onSubmit={handleSave} />}

        <div className={CARD}>
          <button
            type="button"
            onClick={finish}
            className="rounded-lg border border-emerald-500/50 bg-emerald-500/10 px-4 py-2 text-emerald-200"
          >
            Complete Onboarding
          </button>
        </div>
      </div>
    </div>
  );
}
