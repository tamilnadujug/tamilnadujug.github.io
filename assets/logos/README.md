# College Logos

This directory contains the college logos used in the Chapter Leaders page.

## Current Logos

- **sece-logo.svg** - Sri Eshwar College of Engineering, Coimbatore
- **kongu-logo.svg** - Kongu Engineering College, Erode  
- **anna-university-logo.svg** - Anna University, Chennai
- **psg-logo.svg** - PSG College of Technology, Coimbatore

## Logo Specifications

- **Format**: SVG (Scalable Vector Graphics)
- **Size**: 80x80px viewBox
- **Background**: Each logo has a unique colored background
- **Fallback**: If logo fails to load, a generic building icon is displayed

## Adding New Logos

1. Create an SVG file with 80x80px viewBox
2. Use a consistent design style with the existing logos
3. Include college name and location in the design
4. Add the logo path to the JSON file in `data/chapter-leaders.json`
5. Test the logo displays correctly on all screen sizes

## Logo Colors

- **SECE**: Blue gradient (#667eea)
- **Kongu**: Purple gradient (#764ba2)
- **Anna University**: Green (#28a745)
- **PSG**: Red (#dc3545)

## Responsive Behavior

- **Desktop**: 60x60px
- **Tablet**: 50x50px
- **Mobile**: 40x40px
- **Small Mobile**: 40x40px

The logos automatically scale and maintain aspect ratio across all devices.
