// @ts-check

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  textbookSidebar: [
    {
      type: 'category',
      label: 'Module 0: Foundations of Physical AI',
      items: [
        'module-0/chapter-0.1',
        'module-0/chapter-0.2',
        'module-0/chapter-0.3',
        'module-0/chapter-0.4'
      ],
    },
    {
      type: 'category',
      label: 'Module 1: ROS 2 – The Robotic Nervous System',
      items: [
        'module-1/chapter-1.1',
        'module-1/chapter-1.2',
        'module-1/chapter-1.3',
        'module-1/chapter-1.4',
        'module-1/chapter-1.5'
      ],
    },
    {
      type: 'category',
      label: 'Module 2: Digital Twins and Simulation',
      items: [
        'module-2/chapter-2.1',
        'module-2/chapter-2.2',
        'module-2/chapter-2.3',
        'module-2/chapter-2.4'
      ],
    },
    {
      type: 'category',
      label: 'Module 3: NVIDIA Isaac – The AI Robot Brain',
      items: [
        'module-3/chapter-3.1',
        'module-3/chapter-3.2',
        'module-3/chapter-3.3',
        'module-3/chapter-3.4'
      ],
    },
    {
      type: 'category',
      label: 'Module 4: Vision-Language-Action (VLA)',
      items: [
        'module-4/chapter-4.1',
        'module-4/chapter-4.2',
        'module-4/chapter-4.3'
      ],
    },
  ],
};

module.exports = sidebars;